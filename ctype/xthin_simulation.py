from xlink import Xlink
from drawer import Drawer


thin_mode = False
xlink = Xlink()
drawer = Drawer()


def wait_key() -> int:
    key_input: bytes = b' ';
    xlink.begin()
    while not xlink.receive(key_input, 1):  # wait for key input
        xlink.begin()
        drawer.on_tick()
    xlink.end()
    return key_input


def dispatch_key(key: int):
        key_int = int.from_bytes(key, "big")
        xlink.end()
        print(key_int)

        if key_int == 0x40:  # no key pressed
            return

        if thin_mode == False:
            if key_int == 0x39:  # left arrow enter thin mode
                drawer.enable_thin_mode()
                return
        else:
            # thin_mode is True
            if key_int == 0x3f: ## Run/Stop exit thin mode
                drawer.disable_thin_mode()
                return
            
            drawer.on_key(key_int)                


def main_loop():
    # TODO try-except
    while True:
        dispatch_key(wait_key())


if __name__ == "__main__":
    main_loop()
    