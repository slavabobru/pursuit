import pygame as p
import copy
import math
# from player import *
# from enemy import *
from settings import *

p.init()

screen = p.display.set_mode((WIDTH,HEIGHT))
clock = p.time.Clock()
font = p.font.Font('freesansbold.ttf', 20)
level = []
PI = math.pi


p.display.set_caption('Running Balls (beta)')

player_stand = p.transform.scale(p.image.load('res/player.png'), (20,20))
enemy_stand = p.transform.scale(p.image.load('res/boss.png'), (30, 30))
diamond = p.transform.scale(p.image.load('res/diamond.png'), (15, 15))
mine = p.transform.scale(p.image.load('res/mine.png'), (15,15))
blood = p.image.load('res/blood.png')
lightings_images = []
for i in range (1, 5):
    lightings_images.append(p.transform.scale(p.image.load(f'res/molnia{i}.png', (15, 15))))
x_pl = 50
y_pl = 190
direction = 0
x_enemy = 490
y_enemy = 150
direction = 2
flicker = False
turns_allowed = [False, False, False, False]
direction_command = 0
player_speed = 2
score = 0
powerup = False
power_counter = 0
targets = [(x_pl, y_pl), (x_pl, y_pl), (x_pl, y_pl), (x_pl, y_pl)]
enemy_dead = False
enemy_box = False
enemy_speed = 1
startup_counter = 0
lives = 3
game_over = False
game_won = False

class Enemy:
    def __init__(self, x_coord, y_coord, target, speed, img, direct, dead, box, id):
        self.x_pos = x_coord
        self.y_pos = y_coord
        self.center_x = self.x_pos + 22
        self.center_y = self.y_pos + 22
        self.target = target
        self.speed = speed
        self.img = img
        self.direction = direct
        self.dead = dead
        self.in_box = box
        self.id = id
        self.turns, self.in_box = self.check_collisions()
        self.rect = self.draw()

    def draw(self):
        if (not powerup and not self.dead) or (eaten_ghost[self.id] and powerup and not self.dead):
            screen.blit(self.img, (self.x_pos, self.y_pos))

        ghost_rect = p.rect.Rect((self.center_x - 18, self.center_y - 18), (36, 36))
        return ghost_rect

    def check_collisions(self):
        # R, L, U, D
        num1 = ((HEIGHT - 50) // 32)
        num2 = (WIDTH // 30)
        num3 = 15
        self.turns = False
        if 0 < self.center_x // 30 < 29:
            if level[(self.center_y - num3) // num1][self.center_x // num2] == 9:
                self.turns = True

            if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                    or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns = True

            if self.direction == 2 or self.direction == 3:
                if 12 <= self.center_x % num2 <= 18:
                    if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns = True


            if self.direction == 0 or self.direction == 1:
                if 12 <= self.center_x % num2 <= 18:
                    if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns = True


        if 350 < self.x_pos < 550 and 370 < self.y_pos < 480:
            self.in_box = True
        else:
            self.in_box = False
        return self.turns, self.in_box

    def move_enemy(self):
        # r, l, u, d
        # clyde is going to turn whenever advantageous for pursuit
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns:
                self.x_pos += self.speed
            elif not self.turns:
                if self.target > self.y_pos and self.turns:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target < self.y_pos and self.turns:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target < self.x_pos and self.turns:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns:
                if self.target > self.y_pos and self.turns:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos += self.speed
        elif self.direction == 1:
            if self.target > self.y_pos and self.turns:
                self.direction = 3
            elif self.target < self.x_pos and self.turns:
                self.x_pos -= self.speed
            elif not self.turns:
                if self.target > self.y_pos and self.turns:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target < self.y_pos and self.turns:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target > self.x_pos and self.turns:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns:
                if self.target > self.y_pos and self.turns:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target < self.y_pos and self.turns:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos -= self.speed
        elif self.direction == 2:
            if self.target < self.x_pos and self.turns:
                self.direction = 1
                self.x_pos -= self.speed
            elif self.target < self.y_pos and self.turns:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns:
                if self.target > self.x_pos and self.turns:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target < self.x_pos and self.turns:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target > self.y_pos and self.turns:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns:
                if self.target > self.x_pos and self.turns:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target < self.x_pos and self.turns:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos -= self.speed
        elif self.direction == 3:
            if self.target > self.y_pos and self.turns:
                self.y_pos += self.speed
            elif not self.turns:
                if self.target > self.x_pos and self.turns:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target < self.x_pos and self.turns:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target < self.y_pos and self.turns:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns:
                if self.target > self.x_pos and self.turns:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target < self.x_pos and self.turns:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos += self.speed
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos - 30
        return self.x_pos, self.y_pos, self.direction


def draw_misc():
    score_text = font.render(f'Score: {score}', True, 'white')
    screen.blit(score_text, (10, 920))
    if powerup:
        p.draw.circle(screen, 'blue', (140, 930), 15)
    for i in range(lives):
        screen.blit(p.transform.scale(player_stand, (30, 30)), (650 + i * 40, 915))
    if game_over:
        p.draw.rect(screen, 'white', [50, 200, 800, 300],0, 10)
        p.draw.rect(screen, 'dark gray', [70, 220, 760, 260], 0, 10)
        gameover_text = font.render('Game over! Space bar to restart!', True, 'red')
        screen.blit(gameover_text, (100, 300))
    if game_won:
        p.draw.rect(screen, 'white', [50, 200, 800, 300],0, 10)
        p.draw.rect(screen, 'dark gray', [70, 220, 760, 260], 0, 10)
        gameover_text = font.render('Victory! Space bar to restart!', True, 'green')
        screen.blit(gameover_text, (100, 300))


def check_collisions(scor, power, power_count, eaten_ghosts):
    num1 = (HEIGHT - 50) // 32
    num2 = WIDTH // 30
    if 0 < x_pl < 870:
        if level[center_y // num1][center_x // num2] == 1:
            level[center_y // num1][center_x // num2] = 0
            scor += 10
        if level[center_y // num1][center_x // num2] == 2:
            level[center_y // num1][center_x // num2] = 0
            scor += 50
            power = True
            power_count = 0
            eaten_ghosts = False
    return scor, power, power_count, eaten_ghosts



def draw_player():
    # 0-RIGHT, 1-LEFT, 2-UP, 3-DOWN
    if direction == 0:
        screen.blit(player_stand[counter // 5], (x_pl, y_pl))
    elif direction == 1:
        screen.blit(p.transform.flip(player_stand[counter // 5], True, False), (x_pl, y_pl))
    elif direction == 2:
        screen.blit(p.transform.rotate(player_stand[counter // 5], 90), (x_pl, y_pl))
    elif direction == 3:
        screen.blit(p.transform.rotate(player_stand[counter // 5], 270), (x_pl, y_pl))


def check_position(centerx, centery):
    turns = False
    num1 = (HEIGHT - 50) // 32
    num2 = (WIDTH // 30)
    num3 = 15
    # check collisions based on center x and center y of player +/- fudge number
    if centerx // 30 < 29:
        if direction == 0:
            if level[centery // num1][(centerx - num3) // num2] < 3:
                turns = True
        if direction == 1:
            if level[centery // num1][(centerx + num3) // num2] < 3:
                turns = True
        if direction == 2:
            if level[(centery + num3) // num1][centerx // num2] < 3:
                turns = True
        if direction == 3:
            if level[(centery - num3) // num1][centerx // num2] < 3:
                turns = True

        if direction == 2 or direction == 3:
            if 12 <= centerx % num2 <= 18:
                if level[(centery + num3) // num1][centerx // num2] < 3:
                    turns = True
                if level[(centery - num3) // num1][centerx // num2] < 3:
                    turns = True
            if 12 <= centery % num1 <= 18:
                if level[centery // num1][(centerx - num2) // num2] < 3:
                    turns = True
                if level[centery // num1][(centerx + num2) // num2] < 3:
                    turns = True
        if direction == 0 or direction == 1:
            if 12 <= centerx % num2 <= 18:
                if level[(centery + num1) // num1][centerx // num2] < 3:
                    turns = True
                if level[(centery - num1) // num1][centerx // num2] < 3:
                    turns = True
            if 12 <= centery % num1 <= 18:
                if level[centery // num1][(centerx - num3) // num2] < 3:
                    turns = True
                if level[centery // num1][(centerx + num3) // num2] < 3:
                    turns = True
    else:
        turns = True

    return turns


def move_player(play_x, play_y):
    # r, l, u, d
    if direction == 0 and turns_allowed[0]:
        play_x += player_speed
    elif direction == 1 and turns_allowed[1]:
        play_x -= player_speed
    if direction == 2 and turns_allowed[2]:
        play_y -= player_speed
    elif direction == 3 and turns_allowed[3]:
        play_y += player_speed
    return play_x, play_y


def get_targets(enemy_x, enemy_y):
    if x_pl < 450:
        runaway_x = 900
    else:
        runaway_x = 0
    if y_pl < 450:
        runaway_y = 900
    else:
        runaway_y = 0
    return_target = (380, 400)
    if powerup:
        if not enemy.dead and not eaten_ghost[0]:
            enemy_target = (runaway_x, runaway_y)
        elif not enemy.dead and eaten_ghost[0]:
            if 340 < enemy_x < 560 and 340 < enemy_y < 500:
                enemy_target = (400, 100)
            else:
                enemy_target = (x_pl, y_pl)
        else:
            enemy_target = return_target

    else:
        if not enemy.dead:
            if 340 < x_enemy < 560 and 340 < y_enemy < 500:
                enemy_target = (400, 100)
            else:
                enemy_target = (x_pl, y_pl)
        else:
            enemy_target = return_target

    return enemy_target


run = True
while run:
    clock.tick(fps)
    if counter < 19:
        counter += 1
        if counter > 3:
            flicker = False
    else:
        counter = 0
        flicker = True
    if powerup and power_counter < 600:
        power_counter += 1
    elif powerup and power_counter >= 600:
        power_counter = 0
        powerup = False
        eaten_ghost = False
    if startup_counter < 180 and not game_over and not game_won:
        moving = False
        startup_counter += 1
    else:
        moving = True

    screen.fill(bg_color)
    center_x = x_pl + 23
    center_y = y_pl + 24
    if powerup:
        enemy_speed = 1
    else:
        enemy_speed = 2
    if eaten_ghost[0]:
        enemy_speed[0] = 2
    if eaten_ghost[1]:
        enemy_speed[1] = 2
    if eaten_ghost[2]:
        enemy_speed[2] = 2
    if eaten_ghost[3]:
        enemy_speed[3] = 2
    if enemy_dead:
        enemy_speed[0] = 4

    game_won = True
    for i in range(len(level)):
        if 1 in level[i] or 2 in level[i]:
            game_won = False

    player_circle = p.draw.circle(screen, bg_color, (center_x, center_y), 20, 2)
    draw_player()
    enemy = Enemy(x_enemy, y_enemy, targets, enemy_speed, enemy, enemy_direction, enemy_dead,
                   enemy_box, 0)

    draw_misc()
    targets = get_targets(x_enemy, y_enemy)

    turns_allowed = check_position(center_x, center_y)
    if moving:
        x_pl, y_pl = move_player(x_pl, y_pl)
        if not enemy_dead and not enemy.in_box:
            x_enemy, y_enemy, enemy_direction = enemy.move_enemy()
        else:
            x_enemy, y_enemy, enemy_direction = enemy.move_clyde()

    score, powerup, power_counter, eaten_ghost = check_collisions(score, powerup, power_counter, eaten_ghost)
    # add to if not powerup to check if eaten ghosts
    if not powerup:
        if (player_circle.colliderect(enemy.rect) and not enemy_dead) :
            if lives > 0:
                lives -= 1
                startup_counter = 0
                powerup = False
                power_counter = 0
                x_pl = 450
                y_pl = 663
                direction = 0
                direction_command = 0
                x_enemy = 56
                y_enemy = 58
                enemy_direction = 0
                eaten_ghost = False
                enemy_dead = False
            else:
                game_over = True
                moving = False
                startup_counter = 0
    if powerup and player_circle.colliderect(enemy.rect) and eaten_ghost and not enemy.dead:
        if lives > 0:
            powerup = False
            power_counter = 0
            lives -= 1
            startup_counter = 0
            x_pl = 450
            y_pl = 663
            direction = 0
            direction_command = 0
            x_enemy = 56
            y_enemy = 58
            enemy_direction = 0
            eaten_ghost = False
            enemy_dead = False
        else:
            game_over = True
            moving = False
            startup_counter = 0
    if powerup and player_circle.colliderect(enemy.rect) and not enemy.dead and not eaten_ghost[0]:
        enemy_dead = True
        eaten_ghost[0] = True
        score += (2 ** eaten_ghost.count(True)) * 100

    for event in p.event.get():
        if event.type == p.QUIT:
            run = False
        if event.type == p.KEYDOWN:
            if event.key == p.K_RIGHT:
                direction_command = 0
            if event.key == p.K_LEFT:
                direction_command = 1
            if event.key == p.K_UP:
                direction_command = 2
            if event.key == p.K_DOWN:
                direction_command = 3
            if event.key == p.K_SPACE and (game_over or game_won):
                powerup = False
                power_counter = 0
                lives -= 1
                startup_counter = 0
                x_pl = 450
                y_pl = 663
                direction = 0
                direction_command = 0
                x_enemy = 56
                y_enemy = 58
                enemy_direction = 0
                eaten_ghost = False
                enemy_dead = False
                score = 0
                lives = 3
                game_over = False
                game_won = False

        if event.type == p.KEYUP:
            if event.key == p.K_RIGHT and direction_command == 0:
                direction_command = direction
            if event.key == p.K_LEFT and direction_command == 1:
                direction_command = direction
            if event.key == p.K_UP and direction_command == 2:
                direction_command = direction
            if event.key == p.K_DOWN and direction_command == 3:
                direction_command = direction

    if direction_command == 0 and turns_allowed[0]:
        direction = 0
    if direction_command == 1 and turns_allowed[1]:
        direction = 1
    if direction_command == 2 and turns_allowed[2]:
        direction = 2
    if direction_command == 3 and turns_allowed[3]:
        direction = 3

    if x_pl > 900:
        x_pl = -47
    elif x_pl < -50:
        x_pl = 897

    if enemy.in_box and enemy_dead:
        enemy_dead = False


    p.display.flip()
p.quit()

