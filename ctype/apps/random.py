from base_app import BaseApp
import random
from apps.drawer import Drawer

class RandomApp(BaseApp):

    def on_show(self):
        self.screen.clear()
        self.print_at(str(random.random())[0:5], 17, 5)
        self.print_at("X to quit", 13, 9)
        self.draw()

    def on_key(self, key: int) -> None:
        print(f"key in random {key}")
        if key == 0x17:  # X to exit
            print("Stop Random app")
            Drawer.remove_app(self)
            return
