from kivy.app import App
from kivy.uix.widget import Widget
from random import random as r
from kivy.graphics import *
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.properties import NumericProperty
from kivy.clock import Clock

W,H = 700, 700
TILE = 45
GAME_RES = W * TILE, H * TILE

class ButtonUp:
    def build(self):
        self.btn = ButtonUp(text = "Up")
        self.btn.bind(on_press = self.click)
        pass
    def click(self, run):
        self.btn.run = self.run
class ButtonDown:
    def build(self):
        self.btn = ButtonDown(text = "Down")
        self.btn.bind(on_press = self.click)
        pass
    def click(self, run):
        self.btn.run = self.run
class ButtonRight:
    def build(self):
        self.btn = ButtonRight(text = "Right")
        self.btn.bind(on_press = self.click)
        pass
    def click(self, run):
        self.btn.run = self.run
class ButtonLeft:
    def build(self):
        self.btn = ButtonLeft(text = "Left")
        self.btn.bind(on_press = self.click)
        pass
    def click(self, run):
        self.btn.run = self.run
class Player:
    up = ButtonUp()
    down = ButtonDown()
    right = ButtonRight()
    left = ButtonLeft()
    def _draw(self):
        pass
    def run(self):
        speed = NumericProperty()

    def _update(self):
        pass
    def collecting(self):
        pass
    def auch(self):
        pass
    pass
class Boss:
    def _draw(self):
        pass
    def _move(self):
        pass
    def _update(self):
        pass
    def shoot(self):
        pass
class Diamonds:
    def _draw(self):
        diamond = r.randint()
    def _update(self):
        pass
    def timer(self):
        pass
class Bomba:
    def _draw(self):
        pass
    def _update(self):
        pass
    def boom(self):
        pass
class GridGame(Widget):
    my_player = Player()
    my_boss = Boss()
    my_diamonds = Diamonds()
    my_bomba = Bomba()
    def download_player(self, wid, TILE_W, TILE_H):
        # with wid.canvas:
        #     img = Image(source = "res/player.png", size_hint = (.5, .5), pos_hint = {"center_x": 50, "center_y": 50})
        #     return img
        pass

    def new_diamond(self, wid, TILE_W, TILE_H):
    #     with wid.canvas:
    #         diamond = Image(source = "res/diamond.png", size_hint = (.3, .3), pos_hint = {"center_x": r(60, 630), "center_y": r(230, 490)})
    #         return diamond
        pass
    def download_boss(self, wid, TILE_W, TILE_H):
        pass
    def new_bomba(self, wid, TILE_W, TILE_H):
        pass

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
        # self.root.my_grid.new_diamond(self.root.ids["game_layout_box"], TILE_W, TILE_H)


    def on_window_resize(self, window, width, height):
        self._width = self.root.ids["game_layout"].width
        self._height = self.root.ids["game_layout"].height
        self._width_glass = self._width / 20 * 12
        self._height_glass = self._height - 40
        TILE_W = self._width_glass / W
        TILE_H = self._height_glass / H

        self.root.ids["game_layout_box"].canvas.clear()
        self.root.my_grid.download_player(self.root.ids["game_layout_box"], TILE_W, TILE_H)
        self.root.my_grid.new_diamond(self.root.ids["game_layout_box"], TILE_W, TILE_H)


if __name__ == "__main__":
    PursuitApp().run()

