from base_app import BaseApp
from c64_keys import C64Keys
from widgets import HotKey, Label, Button, Input

class Drawer(BaseApp):
    name = "Drawer"  # TODO tohle nebude fungovat
    
    running_apps: list[BaseApp] = []  ## static
    active_app: BaseApp  ## static
    
    @staticmethod
    def get_active_app() -> BaseApp:
        return Drawer.active_app
    
    @staticmethod
    def set_active_app(app: BaseApp, avoid_show:bool=False) -> None:
        Drawer.active_app = app
        if not avoid_show:
            app.on_show()
    
    @staticmethod
    def set_active_app_by_idx(idx: int) -> None:
        Drawer.active_app = Drawer.running_apps[idx]
        Drawer.active_app.on_show()
    
    @staticmethod
    def add_app(app: BaseApp) -> None:
        Drawer.running_apps.append(app)
        app.on_start()
    
    @staticmethod
    def remove_app(app: BaseApp) -> None:
        app.on_hide()
        app.on_stop()
        Drawer.running_apps.remove(app)
        Drawer.set_active_app_by_idx(0)



    def on_start(self) -> None:
        """Define whole layout"""
        self.add_widget(Label("HONDANI", 17, 5))
        self.add_widget(Label("Press L to list a directory", 6, 10))
        self.add_widget(Label("Press R to show random number", 6, 11))        
        self.add_widget(HotKey(C64Keys.l, callback=self.exec_list))
        self.add_widget(HotKey(C64Keys.r, callback=self.exec_random))
        self.add_widget(Button("List", 6, 12, callback=self.exec_list, focused=True))
        self.add_widget(Button("Random", 6, 13, callback=self.exec_random))
        self.add_widget(Button("Random 2", 6, 14, callback=self.exec_random))
        self.add_widget(Input(6, 15, 10, text="Medlik"))


    def exec_list(self):
        print("Starting application List")
        import apps.list
        app = apps.list.ListApp()
        self.add_app(app)
        self.set_active_app(app)
        
    def exec_random(self):
        print("Starting application Random")
        import apps.random
        app = apps.random.RandomApp()
        self.add_app(app)
        self.set_active_app(app)