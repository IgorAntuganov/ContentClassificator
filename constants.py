import pygame

FPS = 165
WIN_SIZE = 1600, 900
SCREEN_RECT = pygame.Rect((0, 0), WIN_SIZE)
MAX_IMAGE_WIDTH = 900
MAX_IMAGE_HEIGHT = 900

BUTTON_RADIUS = 4
BUTTON_SCREEN_COLLISION_DEFLATION = (-5, -5)
NORMAL_BUTTON_SPRITE_DEFLATION = (-2, -2)
ACTIVE_BUTTON_SPRITE_DEFLATION = (0, -2)
ACTIVE_BUTTON_TEXT_DESCENT = 1
BUTTON_OUTLINE_CREATING_DEFLATION = (-4, -4)
OUTLINE_DARKENING_COEFFICIENT = 0.85
SimpleButton_BORDER_RADIUS = 4


SHADOW_TEXT_OFFSET = (0, 4)
OUTLINE_EXTENT = (2, 2)
HALO_EXTENT = (12, 12)
HALO_POWER = 15
STANDARD_UI_POSITION = (100, 100)
STANDARD_UI_SIZE = (250, 50)
STANDARD_UI_BRIGHT = (220, 220, 220)
STANDARD_UI_DARK = (50, 50, 50)
STANDARD_UI_RED = (230, 20, 20)
SCREEN_FILLING_COLOR = (47, 47, 47)


FOCUS_DEBUG_PRINTING = False
RECENT_DEBUG_PRINTING = True
DRAGGING_DEBUG_PRINTING = False
HOVER_DEBUG_PRINTING = False
HANDLERS_REGISTERING_PRINTING = True

if FOCUS_DEBUG_PRINTING:
    def debug_print(*args): print(*args)
else:
    def debug_print(*args): len(args)

if RECENT_DEBUG_PRINTING:
    def debug_print_1(*args): print(*args)
else:
    def debug_print_1(*args):
        len(args)

if DRAGGING_DEBUG_PRINTING:
    def dragging_debug_print(*args): print(*args)
else:
    def dragging_debug_print(*args):
        len(args)

if HOVER_DEBUG_PRINTING:
    def hover_debug_print(*args): print(*args)
else:
    def hover_debug_print(*args):
        len(args)

if HANDLERS_REGISTERING_PRINTING:
    def handlers_registering_print(*args): print(*args)
else:
    def handlers_registering_print(*args):
        len(args)
