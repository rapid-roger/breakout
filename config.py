import colors

screen_width = 1280
screen_height = 720
background_image = 'images/background1.png'
background = dict(
    level1='images/background1.png',
    level2='images/background2.png',
    level3='images/background3.png',
    level4='images/background4.png'
)

icon_image = 'images/icon.png'

frame_rate = 90

ball_speed = 3
ball_speed_min = 1
ball_speed_max = 8
ball_radius = 12
ball_color = colors.WHITE

font_name = 'Trebuchet MS'
font_size = 20
offset_status_y = 5

brick_width = 90
brick_height = 30
brick_separator = 1
brick_color = colors.MANDARIN
offset_y = offset_status_y + font_size + ball_radius * 1.5

row_count = 5
while (row_count * (brick_height + brick_separator) + offset_y) > (screen_height / 2):
    row_count -= 1

paddle_height = 12
paddle_width = 100
paddle_width_min = paddle_height * 2
paddle_width_max = screen_width / 4
paddle_y_min = screen_height / 2 + ball_radius * 2
paddle_color = colors.WHITE
paddle_speed = 8

text_color = colors.WHITE
initial_lives = 3
offset_score = font_size
offset_level = screen_width / 2 - font_size * 2
offset_lives = screen_width - font_size * 5
start_level = 1

effect_duration = 20

music_volume = 0.075
effects_volume = 1

sound_effects = dict(
    brick_hit='sound_effects/brick_hit.ogg',
    paddle_hit='sound_effects/paddle_hit.ogg',
    wall_hit='sound_effects/wall_hit.ogg',
    floor_hit='sound_effects/floor_hit.ogg'
)

music = dict(
    level1='music/soundtrack1.ogg',
    level2='music/soundtrack2.ogg',
    level3='music/soundtrack3.ogg',
    level4='music/soundtrack4.ogg',
    level_complete='music/level_complete.ogg',
    lose_game='music/lose_game.ogg'
)

button_text_color = colors.WHITE,
button_normal_back_color = colors.INDIANRED1
button_hover_back_color = colors.INDIANRED2
button_pressed_back_color = colors.INDIANRED3

menu_button_w = 80
menu_button_h = 35
menu_offset_x = int(brick_width / 2)
menu_offset_y = screen_height / 2 - menu_button_h
