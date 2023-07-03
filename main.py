import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.clock import Clock
from random import randint

kivy.require('1.11.1')

class Player(Widget):
    def __init__(self, **kwargs):
        super(Player, self).__init__(**kwargs)
        self.size = (10, 10)
        self.pos = (randint(0, Window.width - self.width), randint(0, Window.height - self.height))
        self.velocity_x = 0
        self.velocity_y = 0

    def update(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Проверка столкновения с границами игрового поля
        if self.x < 0:
            self.x = 0
        elif self.x > Window.width - self.width:
            self.x = Window.width - self.width
        if self.y < 0:
            self.y = 0
        elif self.y > Window.height - self.height:
            self.y = Window.height - self.height

class Diamond(Widget):
    def __init__(self, **kwargs):
        super(Diamond, self).__init__(**kwargs)
        self.size = (10, 10)
        self.pos = (randint(0, Window.width - self.width), randint(0, Window.height - self.height))

class Mine(Widget):
    def __init__(self, **kwargs):
        super(Mine, self).__init__(**kwargs)
        self.size = (10, 10)
        self.pos = (randint(0, Window.width - self.width), randint(0, Window.height - self.height))

class Boss(Widget):
    def __init__(self, **kwargs):
        super(Boss, self).__init__(**kwargs)
        self.size = (20, 20)
        self.pos = (randint(0, Window.width - self.width), randint(0, Window.height - self.height))
        self.velocity_x = 0
        self.velocity_y = 0

    def update(self, player):
        # Расчет направления движения к игроку
        dx = player.x - self.x
        dy = player.y - self.y
        distance = (dx ** 2 + dy ** 2) ** 0.5

        if distance < 50:
            # Изменение скорости движения к игроку
            self.velocity_x = dx / distance
            self.velocity_y = dy / distance
        else:
            self.velocity_x = 0
            self.velocity_y = 0

        self.x += self.velocity_x
        self.y += self.velocity_y

        # Проверка столкновения с границами игрового поля
        if self.x < 0:
            self.x = 0
        elif self.x > Window.width - self.width:
            self.x = Window.width - self.width
        if self.y < 0:
            self.y = 0
        elif self.y > Window.height - self.height:
            self.y = Window.height - self.height

class GameScreen(BoxLayout):
    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        self.orientation = 'vertical'

        self.player = Player()
        self.diamonds = []
        self.mines = []
        self.boss = Boss()
        self.score = 0
        self.lives = 5

        # Создание кнопок управления
        control_layout = BoxLayout(size_hint=(1, None), height=100)
        control_layout.add_widget(Button(text='Вправо', on_press=self.move_right))
        control_layout.add_widget(Button(text='Влево', on_press=self.move_left))
        control_layout.add_widget(Button(text='Вверх', on_press=self.move_up))
        control_layout.add_widget(Button(text='Вниз', on_press=self.move_down))

        self.add_widget(control_layout)
        self.add_widget(self.player)

        self.health_label = Label(text='Жизни: {}'.format(self.lives))
        self.score_label = Label(text='Счет: {}'.format(self.score))
        self.add_widget(self.health_label)
        self.add_widget(self.score_label)

        self.generate_diamond()
        self.generate_mine()

        Clock.schedule_interval(self.update, 1.0 / 60.0)
        Clock.schedule_interval(self.generate_diamond, 10)
        Clock.schedule_interval(self.generate_mine, 10)
        Clock.schedule_interval(self.boss_shoot, 5)

    def move_right(self, instance):
        self.player.velocity_x = 5

    def move_left(self, instance):
        self.player.velocity_x = -5

    def move_up(self, instance):
        self.player.velocity_y = 5

    def move_down(self, instance):
        self.player.velocity_y = -5

    def update(self, dt):
        self.player.update()
        self.boss.update(self.player)

        # Проверка столкновения игрока с diamond
        for diamond in self.diamonds:
            if self.player.collide_widget(diamond):
                self.score += 1
                self.score_label.text = 'Счет: {}'.format(self.score)
                self.remove_widget(diamond)
                self.diamonds.remove(diamond)

                if self.score % 10 == 0:
                    self.lives += 1
                    self.player.velocity_x += 1.5
                    self.player.velocity_y += 1.5
                    self.health_label.text = 'Жизни: {}'.format(self.lives)

        # Проверка столкновения игрока с mine
        for mine in self.mines:
            if self.player.collide_widget(mine):
                self.lives -= 1
                self.health_label.text = 'Жизни: {}'.format(self.lives)
                self.remove_widget(mine)
                self.mines.remove(mine)

                if self.lives == 0:
                    self.game_over()

        self.check_game_over()
        self.check_game_win()

    def generate_diamond(self, dt):
        diamond = Diamond()
        self.diamonds.append(diamond)
        self.add_widget(diamond)

    def generate_mine(self, dt):
        mine = Mine()
        self.mines.append(mine)
        self.add_widget(mine)

    def boss_shoot(self, dt):
        self.add_widget(self.boss)

    def game_over(self):
        self.clear_widgets()
        self.add_widget(Label(text='GAME OVER'))

    def check_game_over(self):
        if self.lives == 0:
            self.game_over()

    def check_game_win(self):
        if self.score == 300:
            self.clear_widgets()
            self.add_widget(Label(text='ПОБЕДА'))

class GameApp(App):
    def build(self):
        game = GameScreen()
        return game

GameApp().run()
