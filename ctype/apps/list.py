import os
from base_app import BaseApp
from apps.drawer import Drawer
from c64_keys import C64Keys
from widgets import HotKey, Label


class ListApp(BaseApp):
    name = "List Directory"


    def on_start(self) -> None:
        """Define whole layout"""
        self.add_widget(Label(self.name, 12, 2))
        self.dir_label = Label(".", 0, 6)
        self.add_widget(self.dir_label)
        self.add_widget(Label("Press X to quit", 0, 24))        
        self.add_widget(HotKey(C64Keys.x, callback=self.exec_quit))

    def on_show(self):
        self.dir_label.set_text(os.getcwd())
        super().on_show()

    def exec_quit(self):
        Drawer.remove_app(self)
