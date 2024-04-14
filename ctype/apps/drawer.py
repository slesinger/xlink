from base_app import BaseApp


class Drawer(BaseApp):
    name = "Drawer"  # TODO tohle nebude fungovat
    
    running_apps: list[BaseApp] = []
    active_app: int = 0
    
    def get_active_app(self) -> BaseApp:
        return self.running_apps[self.active_app]
    
    def add_app(self, app: BaseApp, avoid_show:bool=False) -> None:
        self.running_apps.append(app)
        app.on_start()
        if not avoid_show:
            app.on_show()
        
    def remove_app(self, app: BaseApp) -> None:
        app.on_hide()
        app.on_stop()
        self.running_apps.remove(app)

    def on_show(self) -> None:
        self.screen.clear()
        self.print_at("HONDANI", 17, 5)
        self.print_at("Press L to list a directory", 6, 10)
        self.draw()

    
    def on_key(self, key: int) -> None:
        print(f"key in drawer {key}")
        if key == 0x2a:  # L for list
            print("Starting application List")
            import apps.list
            app = apps.list.ListApp()
            self.add_app(app)
            return
            
        if key == 0x11:  # R for random number
            print("Starting application Random")
            import apps.list
            app = apps.list.ListApp()
            self.add_app(app)
            return
