import os
from base_app import BaseApp

class ListApp(BaseApp):
    name = "List Directory"

    def on_show(self):
        self.screen.clear()
        self.print_at(self.name, 17, 5)
        self.print_at(os.getcwd(), 6, 10)
        self.draw()
