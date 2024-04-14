from pydantic import BaseModel
from textel import Textel

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


    def put_char(self, char: str, x: int, y: int) -> None:
        """Put a character at position x, y."""
        self.buffer[y][x].put_char(char)


    def get_changes(self) -> list[GetChangesReturn]:
        """Return a list of Textel objects that have changed since last draw."""
        char = bytearray()
        color = bytearray()
        for y in range(self.TEXT_SCREEN_HEIGHT):
            for x in range(self.TEXT_SCREEN_WIDTH):
                if True or self.buffer[y][x].tainted:  # TODO remove True
                    char.append(self.buffer[y][x].get_petscii())
                    color.append(self.buffer[y][x].color)
        # TODO create RLE protocol for changes
        ch = GetChangesReturn(mem_pos=0, length=len(char), char=bytes(char), color=bytes(color))
        return [ch]
    