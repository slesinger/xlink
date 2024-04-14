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
    cursor: Cursor
  
    def __init__(self):
        self.screen = TextScreen()
        self.screen.clear()
        self.cursor = Cursor()


    def draw(self) -> None:
        """Figure out screen changes and push them to xlink"""
        changes:list[GetChangesReturn] = self.screen.get_changes()
        for change in changes:
            rc1 = xlink.load(C64Mem.ZP01_MEM, self.BANK, self.screen.address + change.mem_pos, change.char, change.length)  # load current xthin screen
            sleep(.5)  # next fails without this
            # rc2 = xlink.load(C64Mem.ZP01_MEM, self.BANK, C64Mem.COLOR_MEM_D800 + change.mem_pos, change.color, change.length)  # load current xthin color
            # sleep(.1)  # next fails without this
            print(f"screen pushed {rc1} {rc1}")
            # self.draw_tty()#what=change.char)
            
            
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
    
    
    def print_at(self, text: str, x: int, y: int) -> None:
        """Print at specified position. Line wraps at end of screen. Does not move cursor."""
        for i in range(len(text)):
            self.screen.put_char(text[i], x + i, y)
    
        
    def poke(self, address: int, value: int) -> int:
        """Write value to address in the target machine memory."""
        return xlink.poke(C64Mem.ZP01_MEM, self.BANK, address, value)

    def load(self, memory: int, address: int, data: bytes, size: int) -> bool:
        """Load size bytes of data obtained from the memory area pointed to by data to address in the C64 memory."""
        return xlink.load(memory, self.BANK, address, data, size)

   
    def save(self, memory: int, address: int, data: bytes, size: int) -> bool:
        """Read size bytes of data beginning from address in the C64 memory and store the result in the memory area pointed to by data. The caller has to make sure that enough memory is allocated for data beforehand."""
        return xlink.save(memory, self.BANK, address, data, size)
    
    def jump(self,memory: int, address: int) -> bool:
        """Jump to address in the target machine memory."""
        return xlink.jump(memory, self.BANK, address)