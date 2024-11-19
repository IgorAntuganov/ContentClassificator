import pygame
from states import ButtonState, MouseWheelState
from commands import TextCommand
import json
from constants import NORMAL_BUTTON_SPRITE_DEFLATION, ACTIVE_BUTTON_SPRITE_DEFLATION
from fonts import fonts_dict
from color_schemes import buttons_color_schemes_dict
from UI_abstracts import JSONable, Draggable, Resizable


class Button(JSONable, Draggable, Resizable):
    def set_size(self, size: tuple[int, int]):
        self.rect.size = size

    def get_size(self) -> tuple[int, int]:
        return self.rect.size

    def recreate_sprites_after_resizing(self):
        self.create_all_sprites()

    def get_rect(self) -> pygame.Rect:
        return self.rect

    def __init__(self, text, command: TextCommand, position, size, path_to_json,
                 colors_key=None,
                 font_key=None,
                 border_radius=7):

        JSONable.__init__(self, path_to_json)
        if JSONable.if_file_save_exists(path_to_json):
            position, size = self.load_adjusted_values_from_json()

        self.rect = pygame.Rect(position, size)
        Draggable.__init__(self, self.rect)

        self.text = text
        self.command = command
        self.border_radius = border_radius

        self.font_key = font_key
        assert font_key in fonts_dict
        self.font = fonts_dict[font_key]
        self.colors_key = colors_key
        assert colors_key in buttons_color_schemes_dict
        self.colors = buttons_color_schemes_dict[colors_key]

        self.current_state = ButtonState.NORMAL
        self.sprites = {}
        self.create_all_sprites()

    def create_all_sprites(self):
        self.sprites = {
            ButtonState.NORMAL: self.create_sprite(self.colors[ButtonState.NORMAL],
                                                   deflation=NORMAL_BUTTON_SPRITE_DEFLATION),
            ButtonState.HOVER: self.create_sprite(self.colors[ButtonState.HOVER]),
            ButtonState.ACTIVE: self.create_sprite(self.colors[ButtonState.ACTIVE],
                                                   deflation=ACTIVE_BUTTON_SPRITE_DEFLATION)
        }

    def create_sprite(self, color, deflation=(0, 0)):
        sprite = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        pygame.draw.rect(sprite, color, sprite.get_rect().inflate(deflation), border_radius=self.border_radius)
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

    def save_to_json(self):
        adjusted_values = {'position': self.rect.topleft,
                           'size': self.rect.size}
        with open(self.path_to_json, 'w') as file:
            json.dump(adjusted_values, file)

    def load_adjusted_values_from_json(self):
        with open(self.path_to_json, 'r') as file:
            adjusted_values = json.load(file)
        return [adjusted_values['position'], adjusted_values['size']]
