from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from base_app import BaseApp
class BaseWidget():
    """Base class for all widgets"""
    
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x: int = x
        self.y: int = y
        self.width: int = width
        self.height: int = height
        self.visible: bool = True
        self.enabled: bool = True
        self.focused: bool = False
        self.focusable: bool = False
        self.parent: BaseApp  # TODO Will be BaseWidget in the future when layouts are implemented
        # self.children: list[BaseWidget] = []
        self.name = ""
        
    def on_tick(self):
        pass
    
    def on_key(self, key: int) -> bool:
        return False
    
    def on_mouse(self, x: int, y: int):
        pass
    
    def on_click(self):
        pass
    
    def on_focus(self):
        self.focused = True
    
    def on_blur(self):
        self.focused = False
    
    def on_show(self, app):
        pass
    
    def on_hide(self):
        pass
    
    def set_name(self, name: str):
        self.name = name
        
    def __str__(self):
        return self.name