from base_app import BaseApp
import random
from apps.drawer import Drawer
from c64_keys import C64Keys
from widgets import HotKey, Label

class RandomApp(BaseApp):

    def on_start(self) -> None:
        """Define whole layout"""
        x_hotkey = HotKey(C64Keys.X, callback=self.exec_quit)
        self.add_widget(Label("Random number", 17, 5))
        self.random_label = Label("0.000", 17, 6)
        self.add_widget(self.random_label)
        self.add_widget(Label("Press X to quit", 6, 11))        
        self.add_widget(x_hotkey)

    def on_show(self):
        self.random_label.set_text(str(random.random())[0:5])
        super().on_show()

    def exec_quit(self):
        print("quiting Random app")
        Drawer.remove_app(self)
