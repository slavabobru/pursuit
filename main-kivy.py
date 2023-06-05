from kivy.app import App
from kivy.uix.widget import Widget


class PursuitGame(Widget):
    pass


class PursuitApp(App):
    def build(self):
        return PursuitGame()

if __name__ == "__main__":
    PursuitApp().run()

