import pygame

import config as c
from game_object import GameObject


class Paddle(GameObject):
    def __init__(self, x, y, w, h, color, offset):
        GameObject.__init__(self, x, y, w, h)
        self.color = color
        self.offset = offset
        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.bounds)

    def handle(self, key):
        if key == pygame.K_LEFT or key == pygame.K_a:
            self.moving_left = not self.moving_left
        elif key == pygame.K_RIGHT or key == pygame.K_d:
            self.moving_right = not self.moving_right
        elif key == pygame.K_UP or key == pygame.K_w:
            self.moving_up = not self.moving_up
        elif key == pygame.K_DOWN or key == pygame.K_s:
            self.moving_down = not self.moving_down

    def update(self):
        dx = 0
        dy = 0
        if self.moving_left:
            dx = -min(self.offset, self.left)
        elif self.moving_right:
            dx = min(self.offset, c.screen_width - self.right)

        if self.moving_up:
            dy = -min(self.offset, self.top - c.paddle_y_min)
        elif self.moving_down:
            dy = min(self.offset, c.screen_height - self.bottom)

        self.move(dx, dy)
