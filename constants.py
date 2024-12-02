import pygame

FPS = 30
WIN_SIZE = 1200, 800
SCREEN_RECT = pygame.Rect((0, 0), WIN_SIZE)
MAX_IMAGE_WIDTH = 800
MAX_IMAGE_HEIGHT = 800
BUTTONS_JSON_FILE = 'buttons.json'

BUTTON_RADIUS = 4
BUTTON_SCREEN_COLLISION_DEFLATION = (-5, -5)
NORMAL_BUTTON_SPRITE_DEFLATION = (-3, -3)
ACTIVE_BUTTON_SPRITE_DEFLATION = (-5, -5)

SHADOW_TEXT_OFFSET = (0, 4)
OUTLINE_EXTENT = (2, 2)
HALO_EXTENT = (16, 16)
HALO_POWER = 2.5
STANDARD_UI_POSITION = (100, 100)
STANDARD_UI_SIZE = (250, 50)
STANDARD_UI_BRIGHT = (220, 220, 220)
STANDARD_UI_DARK = (50, 50, 50)
STANDARD_UI_RED = (230, 20, 20)
SCREEN_FILLING_COLOR = (40, 40, 40)
