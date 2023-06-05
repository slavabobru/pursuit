from main import *

class Enemy():
    def __init__(self, x_boss, y_boss, radius, shot, facing):
        self.x_boss = x_boss
        self.y_boss = y_boss
        self.radius = radius
        self.shot = shot
        self.facing = facing
        self.vel = 15 * facing

    def draw(self, screen):
        p.draw.circle(screen, (0, 0, 0), (self.x_boss, self.y_boss))


class Lightnings(p.sprite.Sprite):
    def __init__(self, pos, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=pos)
        self.speed_up_y = -10
        self.speed_down_y = 10
        self.speed_left_x = -10
        self.speed_right_x = 10

    def update(self):
        self.rect.up_y += self.speed_up_y
        self.rect.down_y += self.speed_down_y
        self.rect.left_x += self.speed_left_x
        self.rect.right_x += self.speed_right_x
        if self.rect.bottom < 0 or self.rect.up > 700 or self.rect.left < 0 or self.rect.right > 700:
            self.kill()
