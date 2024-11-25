import pygame
from fonts import fonts_dict
from UI_abstracts import JSONadjustable, Draggable, Drawable
from states import MouseWheelState
import constants as cnst


class SimpleText(JSONadjustable, Draggable, Drawable):
    def create_sprite(self) -> pygame.Surface:
        text_surface = self.font.render(self.text, True, self.color)
        return text_surface

    def __init__(self, text,  path_to_json: str,
                 font_key=None,
                 color: tuple[int, int, int] = cnst.STANDARD_UI_BRIGHT,
                 position=cnst.STANDARD_UI_POSITION):
        self.position = position
        JSONadjustable.__init__(self, path_to_json, position=position)

        assert font_key in fonts_dict
        self.font = fonts_dict[font_key]
        self.text = text
        self.color = color
        self.sprite = self.create_sprite()

        Draggable.__init__(self, self.position, self.sprite.get_size())

    def handle_event(self, mouse_position,
                     mouse_pressed,
                     mouse_wheel_state: MouseWheelState | None = None,
                     ctrl_alt_shift_array: tuple[bool, bool, bool] = (False,)*3):
        if not self.rect_collidepoint(mouse_position) or not mouse_pressed[2]:  # RMB
            self.dragging = False
        else:
            self.handle_dragging(mouse_position)

    def draw(self, screen: pygame.Surface):
        screen.blit(self.sprite, self.get_rect())


class ShadowedText(SimpleText):
    def __init__(self, text, path_to_json: str,
                 font_key=None,
                 color: tuple[int, int, int] = cnst.STANDARD_UI_BRIGHT,
                 shadow_color: tuple[int, int, int] = cnst.STANDARD_UI_DARK,
                 shadow_offset: tuple[int, int] = cnst.SHADOW_TEXT_OFFSET,
                 position=cnst.STANDARD_UI_POSITION):
        self.shadow_color = shadow_color
        self.shadow_offset = shadow_offset
        SimpleText.__init__(self, text,  path_to_json, font_key, color, position)

    def create_sprite(self) -> pygame.Surface:
        text_surface = self.font.render(self.text, True, self.color)
        shadow_surface = self.font.render(self.text, True, self.shadow_color)
        width, height = text_surface.get_rect().size
        width += abs(self.shadow_offset[0])
        height += abs(self.shadow_offset[1])
        sprite = pygame.Surface((width, height), pygame.SRCALPHA)

        offx = self.shadow_offset[0]
        text_x, shadow_x = (0, offx) if offx > 0 else (abs(offx), 0)
        offy = self.shadow_offset[1]
        text_y, shadow_y = (0, offy) if offy > 0 else (abs(offy), 0)

        sprite.blit(shadow_surface, (shadow_x, shadow_y))
        sprite.blit(text_surface, (text_x, text_y))
        return sprite
