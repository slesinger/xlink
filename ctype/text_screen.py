from pydantic import BaseModel
from textel import Textel
from c64_color import C64Color as Color
from itertools import chain

class GetChangesReturn(BaseModel):
    mem_pos: int
    length: int
    char: bytes
    color: bytes


class TextScreen():

    TEXT_SCREEN_WIDTH = 40
    TEXT_SCREEN_HEIGHT = 25
    TEXT_SCREEN_SIZE = TEXT_SCREEN_WIDTH * TEXT_SCREEN_HEIGHT

    address: int = 0x0400  # TODO plan is to make this dynamic, too much refactor at the moment
    buffer:list[list[Textel]]  # address me as buffer[y][x]

    def __init__(self) -> None:
        self.clear()
        
        
    def clear(self) -> None:
        self.buffer = [[Textel() for _ in range(self.TEXT_SCREEN_WIDTH)] for _ in range(self.TEXT_SCREEN_HEIGHT)]

    def is_tainted(self) -> bool:
        for y in range(self.TEXT_SCREEN_HEIGHT):
            for x in range(self.TEXT_SCREEN_WIDTH):
                if self.buffer[y][x].tainted:
                    return True
        return False
    

    def untaint(self) -> None:
        for y in range(self.TEXT_SCREEN_HEIGHT):
            for x in range(self.TEXT_SCREEN_WIDTH):
                self.buffer[y][x].tainted = False


    def put_char(self, char: str, x: int, y: int, color:Color|None=None) -> None:
        """Put a character at position x, y."""
        if x < 0 or x >= self.TEXT_SCREEN_WIDTH or y < 0 or y >= self.TEXT_SCREEN_HEIGHT:
            return
        self.buffer[y][x].put_char(char, color=color)


    def get_changes(self) -> bytearray|None:
        """Return a list of Textel objects that have changed since last draw.
        Notes to figure out approach:
        - Copy bytes is benefit when 3 or more bytes are the same. Do not use it for less than 3 bytes.
        - Receive bytes always loose one byte comnpared to non-RLE version. No counter-measures. Better not fragment.
        - Skip (max 64cells) requires 1 byte, is benefit when 2 or more bytes can be skipped without update.
        - Set address requires 3 bytes, is benefit if absolute address is required or skip is more than 64 cells.

        Procedure:
        1. Figure out tainted areas as mask. Add parts to list Part starts by tainted cell, skips any untainted cells of length 3 or less. 
        2. For each part, split into partlets of copy or recv types. Copy partlets is such that 3 or more bytes are the same, else use recv type.
        3. Each partlet to be copied to a new list, having start address, length, and type.
        4. Encode the list to RLE format. If first partial does not start at 0, use a set address command first to set start address.
        5. After each partlet, add either skipp address (for <=64 untainted cells) or set address (for >64 untainted cells).

        Costs of commands from cheapest to most expensive (also it is an order of preference):
        1. Skip (1 byte) - for <=64 untainted cells
        2. Copy (1 byte + 1 byte data) - for 3 or more same bytes
        3. Receive (1 byte + n bytes data)

        Structure of the RLE data:
          1 byte: command
          n bytes: data
          repeat command - data until command == 0 is received
        Command byte:
          bit 6-7:
            00: copy following byte n-time (max 63+1 times) (n=bit 0-5)
            01: receive n bytes (max 63+1) as usual (n=bit 0-5)
            10: skip (start) address by n (max 63+1) (n=bit 0-6)
            11: set (start) to absolute address to coming <low nibble> <high nibble> (2 bytes) (bits 0-6 set to 0)
        RLE data must always be NULL terminated at the end of the file.
        """
        char = bytearray()
        color = bytearray()
        # Rearrange 2D buffer to 1D list
        buffer1d:list[Textel] = list(chain.from_iterable(self.buffer)) + 3 * [Textel()]  # add 2 extra cells to avoid out of range
        assert len(buffer1d) == self.TEXT_SCREEN_SIZE + 3
        part_started = False  # if false, we are searching for start of a part; if true, we are searching for end of a part
        current_part = {}  # start (inclusive), end (inclusive), type
        parts = []
        for i in range(self.TEXT_SCREEN_SIZE+1):
            if part_started == False and buffer1d[i].tainted:
                current_part["start"] = i
                part_started = True
                print(f"Part started at {i}")
                continue
            if (part_started == True and buffer1d[i].tainted == False and buffer1d[i+1].tainted == False and buffer1d[i+2].tainted == False) or i == self.TEXT_SCREEN_SIZE:
                current_part["end"] = i-1
                print(f"Part ended at {i-1}")
                part_started = False
                # Add part to list
                parts.append(current_part)
                current_part = {}
        print(parts)

        # Create partlets
        partlets = []
        for part in parts:
            partlet = {}
            length = part["end"] - part["start"] + 1
            if length > 64:  # split into partlets of n max 64 as copy/recv cannot handle more in one command
                start = part["start"]
                while length > 0:
                    partlet = {}
                    partlet["start"] = start
                    partlet["end"] = start + min(64, length) - 1
                    partlet["type"] = "receive"
                    partlets.append(partlet)
                    start += 64
                    length -= 64
            else:
                partlet["start"] = part["start"]
                partlet["end"] = part["end"]
                partlet["type"] = "receive"
                partlets.append(partlet)

        if len(partlets) == 0:
            return None

        # Create RLE data

        # clear screen
        # rle_data = bytearray(b'\x3f\x20\x3f\x20\x3f\x20\x3f\x20\x3f\x20\x3f\x20\x3f\x20\x3f\x20\x3f\x20\x3f\x20\x3f\x20\x3f\x20\x3f\x20\x3f\x20\x3f\x20\x27\x20\xc0\x00\x04')

        rle_data = bytearray()
        # set start address
        current_position = 0  # address 0x0400
        for partlet in partlets:
            # set position
            skip_len = partlet["start"] - current_position
            assert skip_len >= 0 and skip_len <= self.TEXT_SCREEN_SIZE
            if skip_len > 64:
                rle_data.extend(b'\xc0')
                rle_data.extend((self.address + partlet["start"]).to_bytes(2, byteorder='little'))
            elif skip_len > 0:
                rle_data.extend((128 + skip_len).to_bytes(1, byteorder='little'))  # 128 is skip command
            current_position = partlet ["end"] + 1

            if partlet["type"] == "copy":
                pass
            elif partlet["type"] == "receive":
                d = 64 + partlet ["end"] - partlet["start"]  # end is inclusive hence +1 but n for recv command requires -1 => -1+1=0. 64 is added to make it a receive command
                rle_data.extend(d.to_bytes(1, byteorder='big'))  # command receive with n-1 length
                rle_data.extend([buffer1d[i].get_petscii() for i in range(partlet["start"], partlet["end"]+1)]) # actual data

        rle_data.extend(b'\x00')
        print(rle_data)
        return rle_data


