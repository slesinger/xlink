class BaseWidget():
    """Base class for all widgets"""
    
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.visible = True
        self.enabled = True
        self.focused = False
        self.parent = None
        self.children = []
        self.name = ""
        
    def on_tick(self):
        pass
    
    def on_key(self, key: int):
        pass
    
    def on_mouse(self, x: int, y: int):
        pass
    
    def on_click(self):
        pass
    
    def on_show(self, app):
        pass
    
    def on_hide(self):
        pass
    
    def set_name(self, name: str):
        self.name = name
        
    def __str__(self):
        return self.name