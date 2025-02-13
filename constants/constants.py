import pygame

FPS = 60
WIN_SIZE = 1200, 720
SCREEN_RECT = pygame.Rect((0, 0), WIN_SIZE)

IMAGES_FORMATS = ('.png', '.jpg', '.jpeg')
IMAGE_SEQUENCE_BACKGROUND = (205, 155, 70)

BUTTON_RADIUS = 4
BUTTON_SCREEN_COLLISION_DEFLATION = (-5, -5)
NORMAL_BUTTON_SPRITE_DEFLATION = (-2, -2)
ACTIVE_BUTTON_SPRITE_DEFLATION = (0, -2)
ACTIVE_BUTTON_TEXT_DESCENT = 1
BUTTON_OUTLINE_CREATING_DEFLATION = (-4, -4)
OUTLINE_DARKENING_COEFFICIENT = 0.85
SimpleButton_BORDER_RADIUS = 4


SHADOW_TEXT_OFFSET = (1, 2)
OUTLINE_EXTENT = (2, 2)
HALO_EXTENT = (12, 12)
HALO_POWER = 15

STANDARD_UI_POSITION = (100, 100)
STANDARD_UI_SIZE = (250, 50)
STANDARD_UI_BRIGHT = (220, 220, 220)
STANDARD_UI_DARK = (50, 50, 50)
STANDARD_UI_RED = (230, 20, 20)
SCREEN_FILLING_COLOR = (47, 47, 47)
