import pygame
from states import ButtonState, MouseWheelState
from commands import TextCommand
import constants as cnst
from fonts import fonts_dict
from color_schemes import buttons_color_schemes_dict
from UI_abstracts import JSONadjustable, Draggable, Resizable, Drawable


class Button(JSONadjustable, Draggable, Resizable, Drawable):
    def recreate_sprites_after_resizing(self):
        self.create_all_sprites()

    def __init__(self, text, command: TextCommand, path_to_json,
                 position=cnst.STANDARD_UI_POSITION,
                 size=cnst.STANDARD_UI_SIZE,
                 colors_key=None,
                 font_key=None,
                 border_radius=7):
        self.position = position
        self.size = size
        JSONadjustable.__init__(self, path_to_json, position=position, size=size)

        Draggable.__init__(self, self.position, self.size)

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
                                                   deflation=cnst.NORMAL_BUTTON_SPRITE_DEFLATION),
            ButtonState.HOVER: self.create_sprite(self.colors[ButtonState.HOVER]),
            ButtonState.ACTIVE: self.create_sprite(self.colors[ButtonState.ACTIVE],
                                                   deflation=cnst.ACTIVE_BUTTON_SPRITE_DEFLATION)
        }

    def create_sprite(self, color, deflation=(0, 0)):
        sprite = pygame.Surface(self.get_size(), pygame.SRCALPHA)
        pygame.draw.rect(sprite, color, sprite.get_rect().inflate(deflation), border_radius=self.border_radius)
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=sprite.get_rect().center)
        sprite.blit(text_surface, text_rect)
        return sprite

    def draw(self, screen: pygame.Surface):
        screen.blit(self.sprites[self.current_state], self.get_rect())

    def handle_event(self, mouse_position,
                     mouse_pressed,
                     mouse_wheel_state: MouseWheelState | None = None,
                     ctrl_alt_shift_array: tuple[bool, bool, bool] = (False, False, False)) -> None | TextCommand:

        if not self.rect_collidepoint(mouse_position):
            self.current_state = ButtonState.NORMAL
            self.dragging = False
            return

        unpressed = False
        if mouse_pressed[0]:  # LMB
            self.current_state = ButtonState.ACTIVE
        elif mouse_pressed[2]:  # RMB
            self.handle_dragging(mouse_position)
            if (mouse_wheel_state is not None) and (mouse_wheel_state != MouseWheelState.INACTIVE):
                self.handle_size_changing(ctrl_alt_shift_array, mouse_wheel_state)
        else:
            if self.current_state == ButtonState.ACTIVE:
                unpressed = True
            self.current_state = ButtonState.HOVER
            self.dragging = False

        if unpressed:
            return self.command
