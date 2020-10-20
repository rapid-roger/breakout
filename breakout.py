import random
from datetime import datetime, timedelta
import os
import time
import pygame
from pygame.rect import Rect


import config as c
from ball import Ball
from brick import Brick
from button import Button
from game import Game
from paddle import Paddle
from text_object import TextObject
import colors


special_effects = dict(
    long_paddle=(colors.CYBER_YELLOW,
                 lambda g: g.change_paddle_width(c.paddle_width // 2),
                 lambda g: g.change_paddle_width(-c.paddle_width // 2)),
    short_paddle=(colors.MAYA_BLUE,
                  lambda g: g.change_paddle_width(-c.paddle_width // 2),
                  lambda g: g.change_paddle_width(c.paddle_width // 2)),
    fast_ball=(colors.MINT_GREEN,
               lambda g: g.change_ball_speed(1, 1),
               lambda g: g.change_ball_speed(-1, -1)),
    slow_ball=(colors.MIDDLE_BLUE_PURPLE,
               lambda g: g.change_ball_speed(-1, -1),
               lambda g: g.change_ball_speed(1, 1)),
    tripple_points=(colors.RED_MUNSELL,
                    lambda g: g.set_points_per_brick(3),
                    lambda g: g.set_points_per_brick(1)),
    extra_life=(colors.ILLUMINATING_EMERALD,
                lambda g: g.add_life(),
                lambda g: None))


class Breakout(Game):
    def __init__(self):
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        if c.start_level <= len(c.music):
            self.game_level = c.start_level
        else:
            self.game_level = 1
        self.background_image = c.background['level'+str(self.game_level)]

        Game.__init__(self, 'Breakout', c.screen_width, c.screen_height, self.background_image, c.frame_rate)
        self.icon_surf = pygame.image.load(c.icon_image)
        pygame.display.set_icon(self.icon_surf)

        self.sound_effects = {name: pygame.mixer.Sound(sound) for name, sound in c.sound_effects.items()}
        self.music = {name: pygame.mixer.Sound(music) for name, music in c.music.items()}
        for name in self.music:
            self.music[name].set_volume(c.music_volume)

        self.reset_effect = None
        self.effect_start_time = None
        self.score = 0
        self.score_mode = 'NORMAL'
        self.lives = c.initial_lives
        self.start_level = False
        self.paddle = None
        self.bricks = None
        self.ball = None
        self.menu_buttons = []
        self.is_game_running = False
        self.create_objects()
        self.points_per_brick = 1

    def play_pan_sound(self, sound_name):
        sound = self.sound_effects[sound_name]
        pan = self.ball.centerx / c.screen_width

        if pan < 0.5:
            volume_right = max(c.effects_volume * pan, 0.35)
            volume_left = c.effects_volume - volume_right
        else:
            volume_right = min(c.effects_volume * pan, 0.65)
            volume_left = c.effects_volume - volume_right

        pygame.mixer.Channel(1).play(sound)
        pygame.mixer.Channel(1).set_volume(volume_left, volume_right)

    def add_life(self):
        self.lives += 1

    def set_points_per_brick(self, points):
        self.points_per_brick = points

    def change_ball_speed(self, dx, dy):
        speed_x = 0
        speed_y = 0
        if c.ball_speed_min <= abs(dx + self.ball.speed[0]) <= c.ball_speed_max:
            speed_x = dx
        if c.ball_speed_min <= abs(dy + self.ball.speed[1]) <= c.ball_speed_max:
            speed_y = dy
        self.ball.speed = (self.ball.speed[0] + speed_x, self.ball.speed[1] + speed_y)

    def change_paddle_width(self, dx):
        change_x = 0
        if c.paddle_width_min <= dx + self.paddle.width <= c.paddle_width_max:
            change_x = dx
        self.paddle.bounds.inflate_ip(change_x, 0)

    def create_menu(self):
        def on_play(_):
            for btn in self.menu_buttons:
                self.objects.remove(btn)

            self.is_game_running = True
            self.start_level = True

            self.is_game_running = True
            self.start_level = True

        def on_quit(_):
            self.game_over = True
            self.is_game_running = False
            self.game_over = True

        for i, (text, click_handler) in enumerate((('PLAY', on_play), ('QUIT', on_quit))):
            b = Button(c.menu_offset_x,
                       c.menu_offset_y + (c.menu_button_h + 5) * i,
                       c.menu_button_w,
                       c.menu_button_h,
                       text,
                       click_handler,
                       padding=5)
            self.objects.append(b)
            self.menu_buttons.append(b)
            self.mouse_handlers.append(b.handle_mouse_event)

    def create_objects(self):
        self.create_bricks()
        self.create_paddle()
        self.create_ball()
        self.create_labels()
        self.create_menu()

    def create_labels(self):
        score_label = TextObject(c.offset_score,
                                 c.offset_status_y,
                                 lambda: f'SCORE: {self.score}',
                                 c.text_color,
                                 c.font_name,
                                 c.font_size)
        self.objects.append(score_label)
        level_label = TextObject(c.offset_level,
                                 c.offset_status_y,
                                 lambda: f'LEVEL: {self.game_level}',
                                 c.text_color,
                                 c.font_name,
                                 c.font_size)
        self.objects.append(level_label)
        lives_label = TextObject(c.offset_lives,
                                 c.offset_status_y,
                                 lambda: f'LIVES: {self.lives}',
                                 c.text_color,
                                 c.font_name,
                                 c.font_size)
        self.objects.append(lives_label)

    def create_ball(self):
        speed = (random.randint(-1, 1), c.ball_speed)
        self.ball = Ball(c.screen_width // 2,
                         c.screen_height // 2,
                         c.ball_radius,
                         c.ball_color,
                         speed)
        self.objects.append(self.ball)

    def create_paddle(self):
        paddle = Paddle((c.screen_width - c.paddle_width) // 2,
                        c.screen_height - c.paddle_height * 2,
                        c.paddle_width,
                        c.paddle_height,
                        c.paddle_color,
                        c.paddle_speed)

        self.keydown_handlers[pygame.K_LEFT].append(paddle.handle)
        self.keydown_handlers[pygame.K_RIGHT].append(paddle.handle)
        self.keydown_handlers[pygame.K_UP].append(paddle.handle)
        self.keydown_handlers[pygame.K_DOWN].append(paddle.handle)
        self.keyup_handlers[pygame.K_LEFT].append(paddle.handle)
        self.keyup_handlers[pygame.K_RIGHT].append(paddle.handle)
        self.keyup_handlers[pygame.K_UP].append(paddle.handle)
        self.keyup_handlers[pygame.K_DOWN].append(paddle.handle)

        self.keydown_handlers[pygame.K_a].append(paddle.handle)
        self.keydown_handlers[pygame.K_d].append(paddle.handle)
        self.keydown_handlers[pygame.K_w].append(paddle.handle)
        self.keydown_handlers[pygame.K_s].append(paddle.handle)
        self.keyup_handlers[pygame.K_a].append(paddle.handle)
        self.keyup_handlers[pygame.K_d].append(paddle.handle)
        self.keyup_handlers[pygame.K_w].append(paddle.handle)
        self.keyup_handlers[pygame.K_s].append(paddle.handle)

        self.paddle = paddle
        self.objects.append(self.paddle)

    def create_bricks(self):
        w = c.brick_width
        h = c.brick_height
        brick_count = c.screen_width // (w + c.brick_separator) - 1
        offset_x = (c.screen_width - brick_count * (w + c.brick_separator)) // 2

        bricks = []
        for row in range(c.row_count + self.game_level):
            for col in range(brick_count):
                effect = None
                brick_color = c.brick_color
                index = random.randint(0, 25 - self.game_level)
                if index < len(special_effects):
                    brick_color, start_effect_func, reset_effect_func = list(special_effects.values())[index]
                    effect = start_effect_func, reset_effect_func

                brick = Brick(offset_x + col * (w + c.brick_separator),
                              c.offset_y + row * (h + c.brick_separator),
                              w,
                              h,
                              brick_color,
                              effect)
                bricks.append(brick)
                self.objects.append(brick)
        self.bricks = bricks

    def handle_ball_collisions(self):
        def intersect(obj, ball):
            edges = dict(left=Rect(obj.left, obj.top, 1, obj.height),
                         right=Rect(obj.right, obj.top, 1, obj.height),
                         top=Rect(obj.left, obj.top, obj.width, 1),
                         bottom=Rect(obj.left, obj.bottom, obj.width, 1))
            collisions = set(edg for edg, rect in edges.items() if ball.bounds.colliderect(rect))

            if not collisions:
                return None
            else:
                return list(collisions)

        speed_x = self.ball.speed[0]
        speed_y = self.ball.speed[1]

        # Hit paddle
        edge = intersect(self.paddle, self.ball)
        if edge is not None:

            if 'top' in edge:
                if speed_y > 0:
                    self.ball.speed = speed_x, -abs(speed_y)

                    if self.paddle.moving_up and self.paddle.top > c.paddle_y_min:
                        if abs(speed_y) >= c.ball_speed_min:
                            self.change_ball_speed(0, -abs(speed_y * 0.1))
                        else:
                            self.change_ball_speed(0, -c.ball_speed_min)

                    elif self.paddle.moving_left and self.paddle.left > 0 and 'left' not in edge:
                        if abs(speed_x) >= c.ball_speed_min:
                            self.change_ball_speed(-abs(speed_x * 0.1), 0)
                        else:
                            self.change_ball_speed(-c.ball_speed_min, 0)

                    elif self.paddle.moving_right and self.paddle.right < c.screen_width and 'right' not in edge:
                        if abs(speed_x) >= c.ball_speed_min:
                            self.change_ball_speed(abs(speed_x * 0.1), 0)
                        else:
                            self.change_ball_speed(c.ball_speed_min, 0)

                elif speed_y < 0:
                    edge.remove('top')

                if self.paddle.top < self.ball.bottom and self.paddle.bottom <= c.screen_height:
                    if self.paddle.moving_up or self.ball.speed[1] <= -c.ball_speed_max * 0.75:
                        self.paddle.move(0, self.ball.bottom - self.paddle.top)

            elif 'bottom' in edge:
                if speed_y < 0:
                    self.ball.speed = speed_x, abs(speed_y)
                elif speed_y > 0:
                    edge.remove('bottom')

                if self.paddle.bottom > self.ball.top and self.paddle.top >= c.paddle_y_min:
                    if self.paddle.moving_down or self.ball.speed[1] >= c.ball_speed_max * 0.75:
                        self.paddle.move(0, self.ball.top - self.paddle.bottom)

            if 'left' in edge:
                if speed_x > 0:
                    self.ball.speed = -abs(speed_x), speed_y
                elif speed_x < 0:
                    edge.remove('left')

                if self.paddle.left < self.ball.right and self.paddle.right <= c.screen_width:
                    if self.paddle.moving_left or self.ball.speed[0] <= -c.ball_speed_max * 0.75:
                        self.paddle.move(self.ball.right - self.paddle.left, 0)

            elif 'right' in edge:
                if speed_x < 0:
                    self.ball.speed = abs(speed_x), speed_y
                elif speed_x > 0:
                    edge.remove('right')

                if self.paddle.right > self.ball.left and self.paddle.left >= 0:
                    if self.paddle.moving_right or self.ball.speed[0] >= c.ball_speed_max * 0.75:
                        self.paddle.move(self.ball.left - self.paddle.right, 0)

        if edge:
            self.play_pan_sound('paddle_hit')
            if abs(self.ball.speed[0]) >= c.ball_speed_max * 0.75 \
                    or abs(self.ball.speed[1]) >= c.ball_speed_max * 0.75:
                self.score += 1
                self.ball.color = colors.PICTORIAL_CARMINE
            else:
                self.ball.color = c.ball_color

        # Hit floor
        if self.ball.top > c.screen_height:
            self.lives -= 1
            self.objects.remove(self.ball)
            self.paddle.move((c.screen_width - c.paddle_width) / 2 - self.paddle.left,
                             c.screen_height - c.paddle_height * 2 - self.paddle.top)
            if self.lives == 0:
                self.game_over = True
            else:
                self.play_pan_sound('floor_hit')
                self.create_ball()
                self.ball.color = c.ball_color

        # Hit ceiling
        if self.ball.top < 0:
            self.play_pan_sound('wall_hit')
            self.ball.speed = (speed_x, abs(speed_y))

        # Hit wall
        if self.ball.left < 0:
            self.play_pan_sound('wall_hit')
            self.ball.speed = (abs(speed_x), speed_y)
        elif self.ball.right > c.screen_width:
            self.play_pan_sound('wall_hit')
            self.ball.speed = (-abs(speed_x), speed_y)

        # Hit brick
        for brick in self.bricks:
            edge = intersect(brick, self.ball)
            if edge is not None:
                if 'top' in edge:
                    if speed_y > 0:
                        self.ball.speed = speed_x, -abs(speed_y)
                    elif speed_y < 0:
                        edge.remove('top')

                if 'bottom' in edge:
                    if speed_y < 0:
                        self.ball.speed = speed_x, abs(speed_y)
                    elif speed_y > 0:
                        edge.remove('bottom')

                if 'left' in edge:
                    if speed_x > 0:
                        self.ball.speed = -abs(speed_x), speed_y
                    elif speed_x < 0:
                        edge.remove('left')

                if 'right' in edge:
                    if speed_x < 0:
                        self.ball.speed = abs(speed_x), speed_y
                    elif speed_x > 0:
                        edge.remove('right')

                if edge is not None:
                    self.play_pan_sound('brick_hit')
                    self.bricks.remove(brick)
                    self.objects.remove(brick)
                    self.score += self.points_per_brick

                    if brick.special_effect is not None:
                        # Reset previous effect if any
                        if self.reset_effect is not None:
                            self.reset_effect(self)

                        # Trigger special effect
                        self.effect_start_time = datetime.now()
                        brick.special_effect[0](self)
                        # Set current reset effect function
                        self.reset_effect = brick.special_effect[1]

    def update(self):
        if not self.is_game_running:
            return

        if self.start_level:
            self.start_level = False
            self.objects.remove(self.paddle)
            self.create_paddle()
            self.music['level' + str(self.game_level)].play(loops=-1, fade_ms=10000)
            self.background_image = pygame.image.load(c.background['level' + str(self.game_level)])

        if not self.bricks:
            self.music['level'+str(self.game_level)].fadeout(1000)
            self.music['level_complete'].play()
            self.objects.remove(self.ball)

            if self.game_level < len(c.background):
                self.show_message('Level ' + str(self.game_level) + ' completed!', centralized=True)
                self.game_level += 1
                self.create_bricks()
                self.create_ball()
                self.start_level = True
            else:
                self.show_message('You win!', centralized=True)
                self.is_game_running = False
                self.game_over = True
                return

        # Reset special effect if needed
        if self.reset_effect:
            if datetime.now() - self.effect_start_time >= timedelta(seconds=c.effect_duration):
                self.reset_effect(self)
                self.reset_effect = None

        self.handle_ball_collisions()
        super().update()

        if self.game_over:
            self.music['level'+str(self.game_level)].fadeout(1000)
            self.music['lose_game'].play()
            self.show_message('GAME OVER!', centralized=True)

    def show_message(self, text, color=colors.WHITE, font_name='Arial', font_size=50, centralized=False):
        message = TextObject(c.screen_width // 2, c.screen_height // 2, lambda: text, color, font_name, font_size)
        self.draw()
        message.draw(self.surface, centralized)
        pygame.display.update()
        time.sleep(4)


def main():
    Breakout().run()


if __name__ == '__main__':
    main()
