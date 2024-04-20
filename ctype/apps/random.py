from base_app import BaseApp
import random
from apps.drawer import Drawer
from c64_keys import C64Keys
from widgets import HotKey, Label

class RandomApp(BaseApp):

    def on_start(self) -> None:
        """Define whole layout"""
        self.add_widget(Label("Keyboard press", 10, 2))
        self.random_label = Label("0.000", 26, 2)
        self.add_widget(self.random_label)
        self.add_widget(Label("Press X to quit", 0, 24))        
        self.add_widget(HotKey(C64Keys.X, callback=self.exec_quit))

    def on_show(self):
        # self.random_label.set_text(str(random.random())[0:5])
        super().on_show()

    def on_key(self, key: int) -> None:
        c64key = C64Keys.get_key_by_idx(key)
        print(f"handling key {type(key)}")
        self.random_label.set_text(c64key.name)
        self.on_show()
            
    def exec_quit(self):
        print("quiting Random app")
        Drawer.remove_app(self)
