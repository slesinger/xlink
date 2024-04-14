from base_app import BaseApp
import random

class RandomApp(BaseApp):
    name = "Random Number"

    def on_show(self):
        self.screen.clear()
        self.print_at(str(random.random()), 17, 5)
        self.draw()
