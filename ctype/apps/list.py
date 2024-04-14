import os
from base_app import BaseApp
from apps.drawer import Drawer
from c64_keys import C64Keys
from widgets import HotKey, Label

class ListApp(BaseApp):
    name = "List Directory"


    def on_start(self) -> None:
        """Define whole layout"""
        x_hotkey = HotKey(C64Keys.X, callback=self.exec_quit)
        self.add_widget(Label(self.name, 17, 5))
        self.dir_label = Label(".", 17, 6)
        self.add_widget(self.dir_label)
        self.add_widget(Label("Press X to quit", 6, 11))        
        self.add_widget(x_hotkey)

    def on_show(self):
        self.dir_label.set_text(os.getcwd())
        super().on_show()

    def exec_quit(self):
        print("quiting List Dir app")
        Drawer.remove_app(self)
