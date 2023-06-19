from kivy.app import App
from kivy.uix.widget import Widget
from random import random as r
from kivy.graphics import *
from kivy.core.window import Window
from kivy.uix.image import Image

W,H = 700, 700
TILE = 45
GAME_RES = W * TILE, H * TILE

class GridGame(Widget):
    def download_player(self, wid, TILE_W, TILE_H):
        with wid.canvas:
            img = Image(source = "res/player.png", size_hint = (.5, .5), pos_hint = {"center_x": 50, "center_y": 50})
            return img

class PursuitGame(Widget):
    my_grid = GridGame()


class PursuitApp(App):
    def build(self):
        Window.bind(on_resize = self.on_window_resize)
        return PursuitGame()
    def on_start(self):
        self._width = self.root.ids["game_layout"].width
        self._height = self.root.ids["game_layout"].height
        self._width_glass = self._width / 20 * 12
        self._height_glass = self._height -40
        TILE_W = self._width_glass / W
        TILE_H = self._height_glass / H


        self.root.my_grid.download_player(self.root.ids["game_layout_box"], TILE_W, TILE_H)

    def on_window_resize(self, window, width, height):
        self._width = self.root.ids["game_layout"].width
        self._height = self.root.ids["game_layout"].height
        self._width_glass = self._width / 20 * 12
        self._height_glass = self._height - 40
        TILE_W = self._width_glass / W
        TILE_H = self._height_glass / H

        self.root.ids["game_layout_box"].canvas.clear()
        self.root.my_grid.download_player(self.root.ids["game_layout_box"], TILE_W, TILE_H)

if __name__ == "__main__":
    PursuitApp().run()

