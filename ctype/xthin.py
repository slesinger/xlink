from xlink import Xlink
from drawer import Drawer


thin_mode = False
xlink = Xlink()
drawer = Drawer()


def wait_key() -> int:
    key_input: bytes = b' '
    xlink.begin()
    while not xlink.receive(key_input, 1):  # wait for key input
        xlink.begin()
        drawer.on_tick()
    xlink.end()
    return ord(key_input)


def dispatch_key(key: int):
        xlink.end()
        print(key)

        if key == 0x40:  # no key pressed
            return

        if drawer.thin_mode == False:
            if key == 0x39:  # left arrow enter thin mode
                drawer.enable_thin_mode()
                return
        else:
            # thin_mode is True
            if key == 0x3f: ## Run/Stop exit thin mode
                drawer.disable_thin_mode()
                return
            
            drawer.on_key(key)                


def main_loop():
    # TODO try-except
    while True:
        dispatch_key(wait_key())


if __name__ == "__main__":
    main_loop()
    