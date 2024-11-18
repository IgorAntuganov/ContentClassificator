import pygame
from states import ButtonState, MouseWheelState
from commands import TextCommand
import json
import os
from constants import BUTTON_COLOR_DICT2
from fonts import fonts_dict
from UI_abstracts import Draggable, Resizable


class Button(Draggable, Resizable):
    def set_size(self, size: tuple[int, int]):
        self.rect.size = size

    def get_size(self) -> tuple[int, int]:
        return self.rect.size

    def recreate_sprites_after_resizing(self):
        self.create_all_sprites()

    def get_rect(self) -> pygame.Rect:
        return self.rect

    def __init__(self, text, command: TextCommand, position, size,
                 colors=BUTTON_COLOR_DICT2,
                 font_key=None,
                 radius=7):
        Draggable.__init__(self, position, size)
        self.text = text
        self.command = command
        self.font_key = font_key
        assert font_key in fonts_dict
        self.font = fonts_dict[font_key]
        self.current_state = ButtonState.NORMAL
        self.radius = radius
        self.colors = colors
        self.sprites = {}
        self.create_all_sprites()

    @classmethod
    def from_dict(cls, kwargs):
        return cls(kwargs['text'],
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
        sprite = pygame.Surface(self.rect.size, pygame.SRCALPHA)
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
