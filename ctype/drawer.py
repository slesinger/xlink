from xthin_base import XthinBase
from c64_mem import C64Mem
from c64_color import C64Color as Color

class Drawer(XthinBase):

    backup_screen = bytearray(40*25)
    thin_mode: bool = False
   
    def __init__(self, simulation=False):
        super().__init__()


    def start(self) -> None:
        self.screen.clear()
        self.print_at("HONDANI", 17, 5)
        self.print_at("Press l to list directory", 10, 10)
        self.draw()


    def enable_thin_mode(self) -> None:
        rc = self.poke(C64Mem.FRAME_COLOR_D020, Color.BLACK)  # indicate thin mode enabled
        print(f"enter thin mode {rc}")
        rc = self.save(C64Mem.ZP01_MEM, self.screen.address, self.backup_screen, len(self.backup_screen))  # save screen memory (40x25, 1 byte per character, 1 byte per color)
        print(f"saved screen {rc}")
        self.start()
        self.thin_mode = True


    def disable_thin_mode(self) -> None:
        rc = self.load(C64Mem.ZP01_MEM, self.screen.address, self.backup_screen, len(self.backup_screen))  # load screen memory (40x25, 1 byte per character, 1 byte per color)
        print(f"restored {rc}")
        rc = self.poke(C64Mem.FRAME_COLOR_D020, Color.LIGHT_BLUE)  # indicate thin mode disabled
        print(f"exited {rc}")
        self.thin_mode = False


    def on_tick(self) -> None:
        # print("tick")
        pass
    
    
    def on_key(self, key: int) -> None:
        print(f"key in drawer {key}")
        if key == 0x2a:  # l for list
            print("execute list")
        else:
            print(f"key {key} not handled")

