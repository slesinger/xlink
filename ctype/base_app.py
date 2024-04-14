from xthin_toolkit import XthinToolkit

class BaseApp(XthinToolkit):


    def on_tick(self) -> None:
        """Executed from main loop as often as possible. Can be used for animations"""
        pass


    def on_key(self, key: int) -> None:
        """Executed when a key is pressed. Key is a keyboard code."""
        print(f"unhandled key {key}")


    def on_start(self) -> None:
        """Executed only once when first invoked. Can be used to draw initial screen."""
        pass

    def on_stop(self):
        pass
    
    def on_show(self):
        pass
    
    def on_hide(self):
        pass
    
    def set_name(self, name: str) -> None:
        self.name = name
                
    def __str__(self) -> str:
        return self.name


