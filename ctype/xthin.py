from time import sleep
import traceback
from xlink import Xlink
from xthin_toolkit import XthinToolkit
from text_screen import TextScreen
from c64_mem import C64Mem
from c64_color import C64Color as Color
from c64_keys import C64Keys
import apps.drawer

thin_mode = False
xlink = Xlink()

drawer = apps.drawer.Drawer()
c64 = XthinToolkit()
backup_screen: bytes = b'\1' * TextScreen.TEXT_SCREEN_SIZE  # TODO do also for color # holds C64 screen in order to return from thin back to C64 mode


def on_key(key: int) -> None:
    if key == C64Keys.LEFT_ARROW:  # left arrow for exiting thin mode
        print("exit thin mode requested")
        disable_thin_mode()
        return
    drawer.get_active_app().on_key(key)


def enable_thin_mode() -> None:
    global thin_mode
    # JMP to thin mode in C64 because (#0302) vector is set yet not active to thin mode loop
    rc = c64.jump(C64Mem.ZP01_MEM, 0x0810)
    print(f"C64 to enter thin mode loop, lowercase {rc}")
    sleep(.02)
    
    # TODO this is an example of recovery from a failed call. Make it more reusable
    rc = False
    while rc == False:
        rc = c64.save(C64Mem.ZP01_MEM, TextScreen.address, backup_screen, len(backup_screen))  # save screen memory (40x25, 1 byte per character, 1 byte per color)
        sleep(.1)  # next fails without this
        print(f"saving screen {rc}")
        if rc == False:
            sleep(1)
            c64.poke(C64Mem.FRAME_COLOR_D020, Color.BLACK)
            sleep(1)
        
    drawer.get_active_app().on_show()  # TODO this assumes app is started already
    thin_mode = True


def disable_thin_mode() -> None:
    global thin_mode
    drawer.get_active_app().on_hide()  # TODO this assumes app is started already
    rc = False
    while rc == False:
        rc = c64.load(C64Mem.ZP01_MEM, TextScreen.address, backup_screen, len(backup_screen))  # load screen memory (40x25, 1 byte per character, 1 byte per color)
        sleep(.1)  # next fails without this
        print(f"loading screen {rc}")
        if rc == False:
            sleep(1)
            c64.poke(C64Mem.FRAME_COLOR_D020, Color.BLACK)
            sleep(1)

    # reinstall BASIC loop
    sleep(.02)
    rc = c64.jump(C64Mem.ZP01_MEM, 0x0813)
    print(f"C64 to enter BASIC, upercase {rc}")
    thin_mode = False


def wait_key() -> int:
    key_input: bytes = b' '
    xlink.begin()
    while not xlink.receive(key_input, 1):  # wait for key input
        xlink.begin()
        if thin_mode == True:
            drawer.get_active_app().on_tick()
    xlink.end()
    return ord(key_input)


def dispatch_key(key: int):
    """
    xy111111 key codes  (3a ctrl pressed, 3d ctrl unpressed)
    xy:
    00 key codes
    01 no key + joys
    10 C=
    11 shift

    joys:
    00-jzbcd joys
    j: 0 joy1, 1 joy2
    z: button
    bcd:
    d 0 no move, 1 some move
    c 0 up, 1 down
    b 0 left, 1 right
    """
    xlink.end()
    print(key)

    if key == C64Keys.NO_KEY:  # no key pressed
        return

    if thin_mode == True:
        if key == 0xff:  # C64 was reset  (or SHIFT+RUN/STOP)
            disable_thin_mode()
            return

    if thin_mode == False:
        if key == C64Keys.LEFT_ARROW:  # left arrow enter thin mode
            enable_thin_mode()
            return
    else:
        on_key(key)                


def main_loop():
    while True:
        try:
            dispatch_key(wait_key())
        except Exception as e:
            print(f"Exception: {e}")
            print(traceback.format_exc())


if __name__ == "__main__":
    print("Waiting for C64 to connect...")
    while wait_key() != 0x3d:
        pass
    print("READY.")
    apps.drawer.Drawer.add_app(drawer)
    apps.drawer.Drawer.set_active_app(drawer, avoid_show=True)
    main_loop()
    