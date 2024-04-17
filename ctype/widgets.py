from base_widget import BaseWidget
from c64_keys import C64Keys

class VoidWidget(BaseWidget):
    """A widget that does nothing"""
    def __init__(self):
        super().__init__(0, 0, 0, 0)
        self.visible = False
        self.enabled = False

    def on_tick(self):
        pass

    def on_key(self, key: int):
        pass

    def on_mouse(self, x: int, y: int):
        pass

    def on_click(self):
        pass

    def on_show(self):
        pass

    def on_hide(self):
        pass


class Label(BaseWidget):
    """A simple label"""
    def __init__(self, text: str, x: int, y: int):
        super().__init__(x, y, len(text), 1)
        self.text = text

    def on_show(self, app):
        app.print_at(self.text, self.x, self.y)

    def set_text(self, text: str):
        self.text = text
        self.width = len(text)


class HotKey(BaseWidget):
    """A hotkey that does not have any visual representation, but triggers a callback when pressed"""
    def __init__(self, key: int, callback):
        super().__init__(0, 0, 0, 0)
        self.key = key
        self.callback = callback

    def on_key(self, key: int):
        if key == self.key:  # Global HotKey has higher priority
            self.callback()
            return
            

class Button(BaseWidget):
    """A simple button"""
    def __init__(self, text: str, x: int, y: int, callback, focused=False):
        super().__init__(x, y, len(text), 1)
        self.text = text
        self.callback = callback
        self.focused = focused
        self.focusable = True  # TODO if focused True, make sure all other focusables are False

    def on_show(self, app):
        if self.focused:
            app.print_at(f"<{self.text}>", self.x, self.y)
        else:
            app.print_at(f"[{self.text}]", self.x, self.y)

    def on_key(self, key: int) -> bool:
        """Return True if the key was handled"""
        if key == C64Keys.RETURN and self.focused:
            self.callback()
            return True
        elif key == C64Keys.UP_ARROW:
            assert self.parent is not None
            if self.parent.focus_next_widget():
                # redraw the screen
                self.parent.screen_tainted = True
                return True
        return False

