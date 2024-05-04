from xlink import Xlink
from text_screen import GetChangesReturn
from text_screen import TextScreen
from text_cursor import Cursor
from c64_mem import C64Mem
from time import sleep

xlink = Xlink()

class XthinToolkit():

    BANK = 0x00
    screen: TextScreen
    must_rerender: bool
    cursor: Cursor
  
    def __init__(self):
        self.screen = TextScreen()
        self.screen.clear()
        self.cursor = Cursor()
        self.must_rerender = True

    def clear_screen(self) -> None:
        self.screen.clear()
        self.must_rerender = True

    def draw_to_c64(self) -> None:
        """Figure out screen changes and push them to xlink"""
            
        if not self.screen.is_tainted():
            return
        rle_data = self.screen.get_changes()
        if rle_data:
            rc1 = xlink.load_rle(C64Mem.ZP01_MEM, self.BANK, TextScreen.address, bytes(rle_data), len(rle_data))
            self.screen.untaint()  # set all Textels on screen  tained = False
            sleep(.5)  # next fails without this
            print(f"Pushed screen {rc1}, color {'rc2'}")


    def draw_tty(self, what:bytes=b'') -> None:
        """Draw the screen to the terminal."""
        if len(what) > 0:
            print(what)
        else:
            for y in range(self.screen.TEXT_SCREEN_HEIGHT):
                for x in range(self.screen.TEXT_SCREEN_WIDTH):
                    print(self.screen.buffer[y][x].get_ascii(), end="")
        print("---")
    
    
    def print(self, text: str) -> None:
        """Print at current cursor position. Line wraps at end of screen."""
        pass
    
    
    def print_at(self, text: str, x: int, y: int, color=None) -> None:
        """Print at specified position. Line wraps at end of screen. Does not move cursor."""
        for i in range(len(text)):
            self.screen.put_char(text[i], x + i, y, color=color)
    
        
    def poke(self, address: int, value: int) -> int:
        """Write value to address in the target machine memory."""
        return xlink.poke(C64Mem.ZP01_MEM, self.BANK, address, value)


    def load(self, memory: int, address: int, data: bytes, size: int) -> bool:
        """Load size bytes of data obtained from the memory area pointed to by data to address in the C64 memory."""
        return xlink.load(memory, self.BANK, address, data, size)


    def load_rle(self, memory: int, address: int, rle_data: bytes, size: int) -> bool:
        """Load RLE encoded data obtained from the memory area pointed to by data to address in the C64 memory. Size is of the RLE buffer."""
        return xlink.load_rle(memory, self.BANK, address, rle_data, size)


    def save(self, memory: int, address: int, data: bytes, size: int) -> bool:
        """Read size bytes of data beginning from address in the C64 memory and store the result in the memory area pointed to by data. The caller has to make sure that enough memory is allocated for data beforehand."""
        return xlink.save(memory, self.BANK, address, data, size)
    
    def jump(self,memory: int, address: int) -> bool:
        """Jump to address in the target machine memory."""
        return xlink.jump(memory, self.BANK, address)