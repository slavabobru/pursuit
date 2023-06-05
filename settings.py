import random as r

# display
HEIGHT = 700
WIDTH = 700

fps = 60

bg_color = (250, 250, 250)

# координаты
#player
x_pl = 50
y_pl = 190

#enemy
x_enemy = 490
y_enemy = 150

#diamond
x_d = (r.randint(0, WIDTH - 20))
y_d = (r.randint(0, HEIGHT - 20))

#mine
x_m = (r.randint(0, WIDTH - 20))
y_m = (r.randint(0, HEIGHT - 20))

#speed enemy
speed = 3

player_alive = True
boss_alive = True
mina_alive = True
diamond_alive = True

left = False
right = False
up = False
down = False

game = True

boss_is_near = False

animation_count = 0
