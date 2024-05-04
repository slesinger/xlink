from xthin_toolkit import XthinToolkit
from base_widget import BaseWidget
from widgets import HotKey, VoidWidget

class BaseApp(XthinToolkit):
    
    widgets: list[BaseWidget]
    active: bool = False

    def __init__(self):
        self.widgets = []  # Must be explicitly initialized
        super().__init__()

    def on_tick(self) -> None:
        """Executed from main loop as often as possible. Can be used for animations"""
        pass


    def on_key(self, key: int) -> None:
        """Executed when a key is pressed. Key is a keyboard code."""
        print(f"handling key {key}")
        for widget in self.widgets:
            if isinstance(widget, HotKey):
                widget.on_key(key)
            elif widget.focused:
                if widget.on_key(key):
                    break  # return if key was fulfilled
        if self.must_rerender and self.active:
            self.on_show()


    def on_start(self) -> None:
        """Executed only once when first invoked. Can be used to draw initial screen."""
        pass

    def on_stop(self):
        """Execute when the app is removed from the stack. Can be used to clean up resources."""
        pass
    
    def on_show(self):
        """Render widgets to the screen."""
        self.render_widgets()
        self.draw_to_c64()
    
    def on_hide(self):
        pass
    
    def focus_next_widget(self) -> BaseWidget|None:
        next_idx = 999
        for i, widget in enumerate(self.widgets):
            if widget.focused:
                widget.on_blur()
                next_idx = i
            else:
                if widget.focusable and next_idx < i:
                    widget.on_focus()
                    return widget
        # if nothing has been focused, focus the first focusable widget
        for i, widget in enumerate(self.widgets):
            if widget.focusable:
                widget.on_focus()
                return widget

    
    def set_name(self, name: str) -> None:
        self.name = name
    
    def add_widget(self, widget: BaseWidget) -> None:
        widget.parent = self
        self.widgets.append(widget)
        
    def render_widgets(self) -> None:
        for widget in self.widgets:
            if widget.visible:
                widget.on_show(self)
                
    def __str__(self) -> str:
        return self.name


