import pygame

WIN_SIZE = 1200, 800
SCREEN_RECT = pygame.Rect((0, 0), WIN_SIZE)
MAX_IMAGE_WIDTH = 800
MAX_IMAGE_HEIGHT = 800
BUTTONS_JSON_FILE = 'buttons.json'

from states import ButtonState
BUTTON_COLOR_DICT1 = {
    ButtonState.NORMAL: (235, 165, 5),
    ButtonState.HOVER: (235, 190, 0),
    ButtonState.ACTIVE: (180, 155, 5)
}
BUTTON_COLOR_DICT2 = {
    ButtonState.NORMAL: (224, 245, 245),
    ButtonState.HOVER: (255, 228, 225),
    ButtonState.ACTIVE: (216, 191, 216)
}
BUTTON_SCREEN_COLLISION_DEFLATION = (-10, -10)
