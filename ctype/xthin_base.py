from xlink import Xlink
from text_screen import TextScreen, GetChangesReturn
from text_cursor import Cursor
from c64_mem import C64Mem

xlink = Xlink()

class XthinBase():

    BANK = 0x00
    screen: TextScreen
    cursor: Cursor
   
    def __init__(self) -> None:
        self.screen = TextScreen()
        self.screen.clear()

    
    def on_tick(self) -> None:
        """Executed from main loop as often as possible. Can be used for animations"""
        print("unhandled tick")
        pass


    def on_key(self, key: int) -> None:
        """Executed when a key is pressed. Key is a keyboard code."""
        print(f"unhandled key {key}")


    def start(self) -> None:
        """Executed only once when first invoked. Can be used to draw initial screen."""
        print("unhandled start of application")
        pass


    def draw(self) -> None:
        """Figure out screen changes and push them to xlink"""
        changes:list[GetChangesReturn] = self.screen.get_changes()
        for change in changes:
            rc1 = xlink.load(C64Mem.ZP01_MEM, self.BANK, self.screen.address + change.mem_pos, change.char, self.screen.TEXT_SCREEN_SIZE)  # load current xthin screen
            rc2 = xlink.load(C64Mem.ZP01_MEM, self.BANK, C64Mem.COLOR_MEM_D800 + change.mem_pos, change.color, self.screen.TEXT_SCREEN_SIZE)  # load current xthin screen
            print(f"screen pushed {rc1} {rc2}")
            # self.draw_tty()
            
            
    def draw_tty(self) -> None:
        """Draw the screen to the terminal."""
        for y in range(self.screen.TEXT_SCREEN_HEIGHT):
            for x in range(self.screen.TEXT_SCREEN_WIDTH):
                print(self.screen.buffer[y][x].get_ASCII(), end="")
            print()
    
    
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

    def load(self, memory: int, address: int, data: bytearray, size: int) -> bool:
        """Load size bytes of data obtained from the memory area pointed to by data to address in the C64 memory."""
        return xlink.load(memory, self.BANK, address, bytes(data), size)

   
    def save(self, memory: int, address: int, data: bytearray, size: int) -> bool:
        """Read size bytes of data beginning from address in the C64 memory and store the result in the memory area pointed to by data. The caller has to make sure that enough memory is allocated for data beforehand."""
        return xlink.save(memory, self.BANK, address, bytes(data), size)