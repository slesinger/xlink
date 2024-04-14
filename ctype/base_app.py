from xthin_toolkit import XthinToolkit
from base_widget import BaseWidget
from widgets import HotKey, VoidWidget

class BaseApp(XthinToolkit):
    
    widgets: list[BaseWidget] = []
    active_widget: BaseWidget = VoidWidget()


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
                widget.on_key(key)


    def on_start(self) -> None:
        """Executed only once when first invoked. Can be used to draw initial screen."""
        pass

    def on_stop(self):
        """Execute when the app is removed from the stack. Can be used to clean up resources."""
        pass
    
    def on_show(self):
        self.screen.clear()
        self.render_widgets()
        self.draw()
    
    def on_hide(self):
        pass
    
    def set_name(self, name: str) -> None:
        self.name = name
    
    def add_widget(self, widget: BaseWidget) -> None:
        self.widgets.append(widget)
        
    def render_widgets(self) -> None:
        for widget in self.widgets:
            if widget.visible:
                widget.on_show(self)
                
    def __str__(self) -> str:
        return self.name


