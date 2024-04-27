from base_app import BaseApp
from c64_keys import C64Keys
from widgets import HotKey, Label, Button, Input
from c64_color import C64Color as Color

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
        self.add_widget(Label("HONDANI", 17, 5, color=Color.YELLOW))
        self.add_widget(HotKey(C64Keys.t, callback=self.test_rle))
        self.add_widget(HotKey(C64Keys.l, callback=self.exec_list))
        self.add_widget(HotKey(C64Keys.r, callback=self.exec_random))
        self.add_widget(Button("Random", 6, 10, callback=self.exec_random, focused=True))
        self.add_widget(Button("File Manager", 6, 11, callback=self.exec_list))
        self.add_widget(Input(6, 15, 10, text="Medlik", focused=False))

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

    def test_rle(self):
        print("Testing RLE")
        from c64_mem import C64Mem
        from text_screen import TextScreen
        # data = b'\x04\x01\x01\x02\x00'  # copy bytes: aaaaabb
        # data = b'\x42\x11\x12\x13\x00'  # receive bytes: qrs
        # data = b'\x04\x01\x01\x02\x42\x11\x12\x13\x00'  # copy bytes, recv bytes: aaaaabbqrs
        # data = b'\x42\x11\x12\x13\x04\x01\x01\x02\x00'  # recv bytes, copy bytes: qrsaaaaabb
        # data = b'\x04\x01\x82\x42\x11\x12\x13\x00'  # copy, skip 3, recv: aaaaa>>>qrs
        data = b'\x04\x01\xc0\x28\x04\x42\x11\x12\x13\x00'  # copy, set 0428, recv: aaaaa\nqrs
        self.load_rle(C64Mem.ZP01_MEM, TextScreen.address, data, len(data))
