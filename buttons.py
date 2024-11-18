import pygame
from states import ButtonState, MouseWheelState
from abc import ABC
from commands import TextCommand
import json
import os
from constants import *
from fonts import fonts_dict


class Button(ABC):
    def __init__(self, text, command: TextCommand, position, size,
                 colors=BUTTON_COLOR_DICT2,
                 font_key=None,
                 radius=7,):
        self.position = position
        self.dragging = False
        self.dragging_start_mouse = None
        self.dragging_start_top_left = None

        self.text = text
        self.size = size
        self.rect = pygame.Rect(position, size)

        self.command = command

        self.font_key = font_key
        assert font_key in fonts_dict
        self.font = fonts_dict[font_key]

        self.current_state = ButtonState.NORMAL

        self.radius = radius
        self.colors = colors  # Словарь с ключами: ButtonState.NORMAL, ButtonState.HOVER, ButtonState.ACTIVE
        self.sprites = {}
        self.create_all_sprites()

    @classmethod
    def from_dict(cls, kwargs):
        return Button(kwargs['text'],
                      TextCommand(kwargs['command']),
                      kwargs['position'],
                      kwargs['size'])

    def create_all_sprites(self):
        self.sprites = {
            ButtonState.NORMAL: self.create_sprite(self.colors[ButtonState.NORMAL]),
            ButtonState.HOVER: self.create_sprite(self.colors[ButtonState.HOVER]),
            ButtonState.ACTIVE: self.create_sprite(self.colors[ButtonState.ACTIVE])
        }

    def create_sprite(self, color):
        sprite = pygame.Surface(self.size, pygame.SRCALPHA)
        pygame.draw.rect(sprite, color, sprite.get_rect(), border_radius=self.radius)
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=sprite.get_rect().center)
        sprite.blit(text_surface, text_rect)
        return sprite

    def draw(self, screen):
        screen.blit(self.sprites[self.current_state], self.rect)

    def handle_event(self, mouse_position,
                     mouse_pressed,
                     can_be_dragged=True,
                     mouse_wheel_state: MouseWheelState | None = None,
                     ctrl_alt_shift_array: tuple[bool, bool, bool] = (False, False, False)) -> None | TextCommand:
        unpressed = False
        if self.rect.collidepoint(mouse_position):
            if mouse_pressed[0]:  # LMB
                self.current_state = ButtonState.ACTIVE
            elif mouse_pressed[2] and can_be_dragged:  # RMB
                self.handle_dragging(mouse_position)
                if (self.dragging and
                        mouse_wheel_state is not None and
                        mouse_wheel_state != MouseWheelState.INACTIVE):
                    self.handle_size_changing(ctrl_alt_shift_array, mouse_wheel_state)
            else:
                if self.current_state == ButtonState.ACTIVE:
                    unpressed = True
                self.current_state = ButtonState.HOVER
                self.dragging = False
        else:
            self.current_state = ButtonState.NORMAL
            self.dragging = False

        if unpressed:
            return self.command

    def handle_dragging(self, mouse_position):
        if not self.dragging:
            self.dragging = True
            self.dragging_start_mouse = mouse_position
            self.dragging_start_top_left = self.rect.topleft
        else:
            last_position = self.rect.topleft
            offset_x = mouse_position[0] - self.dragging_start_mouse[0]
            offset_y = mouse_position[1] - self.dragging_start_mouse[1]
            self.rect.x = self.dragging_start_top_left[0] + offset_x
            self.rect.y = self.dragging_start_top_left[1] + offset_y
            if not SCREEN_RECT.contains(self.rect.inflate(*BUTTON_SCREEN_COLLISION_DEFLATION)):
                self.dragging = False
                self.rect.topleft = last_position

    def handle_size_changing(self, ctrl_alt_shift_array, mouse_wheel_state):
        sign = mouse_wheel_state.value
        if ctrl_alt_shift_array[2]:
            value = sign * 5
        else:
            value = sign

        if ctrl_alt_shift_array[0]:
            self.size = self.size[0] + value, self.size[1]
        if ctrl_alt_shift_array[1]:
            self.size = self.size[0], self.size[1] + value

        self.create_all_sprites()
        self.rect.size = self.size


def load_button_positions(file_path: str):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    return []


def save_button_positions(buttons: list[Button], file_path: str):
    positions = [{'text': button.text,
                  'command': button.command.to_json(),
                  'position': button.rect.topleft,
                  'size': button.rect.size,
                  'font_key': button.font_key}
                 for button in buttons]
    with open(file_path, 'w') as file:
        json.dump(positions, file)
