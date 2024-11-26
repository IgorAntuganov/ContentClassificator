import math
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


class OutlinedText(SimpleText):
    def __init__(self, text, path_to_json: str,
                 font_key=None,
                 color: tuple[int, int, int] = cnst.STANDARD_UI_BRIGHT,
                 outline_color: tuple[int, int, int] = cnst.STANDARD_UI_RED,
                 outline_extent: tuple[int, int] = cnst.OUTLINE_EXTENT,
                 position=cnst.STANDARD_UI_POSITION):
        self.outline_color = outline_color
        self.outline_extent = outline_extent
        SimpleText.__init__(self, text,  path_to_json, font_key, color, position)

    def create_sprite(self) -> pygame.Surface:
        text_surface = self.font.render(self.text, True, self.color)
        outline_surface = self.font.render(self.text, True, self.outline_color)

        width, height = text_surface.get_rect().size
        halo_w, halo_h = self.outline_extent
        width += halo_w * 2
        height += halo_h * 2
        sprite = pygame.Surface((width, height), pygame.SRCALPHA)

        for i in range(halo_w*2+1):
            for j in range(halo_h*2+1):
                sprite.blit(outline_surface, (i, j))
        sprite.blit(text_surface, (halo_w, halo_h))
        return sprite


class HaloText(SimpleText):
    def __init__(self, text, path_to_json: str,
                 font_key=None,
                 color: tuple[int, int, int] = cnst.STANDARD_UI_BRIGHT,
                 halo_color: tuple[int, int, int] = cnst.STANDARD_UI_RED,
                 halo_extent: tuple[int, int] = cnst.HALO_EXTENT,
                 halo_power: int = cnst.HALO_POWER,
                 position=cnst.STANDARD_UI_POSITION):
        self.halo_color = halo_color
        self.halo_extent = halo_extent
        self.halo_power = halo_power
        SimpleText.__init__(self, text,  path_to_json, font_key, color, position)

    def create_sprite(self) -> pygame.Surface:
        text_surface = self.font.render(self.text, True, self.color)
        halo_surface = self.font.render(self.text, True, self.halo_color)

        width, height = text_surface.get_rect().size
        halo_w, halo_h = self.halo_extent
        max_distance = (halo_w ** 2 + halo_h ** 2) ** .5
        width += halo_w * 2
        height += halo_h * 2
        sprite = pygame.Surface((width, height), pygame.SRCALPHA)

        for i in range(halo_w*2+1):
            for j in range(halo_h*2+1):
                distance = ((halo_w-i) ** 2 + (halo_h-j) ** 2) ** .5
                part = 1-(distance / max_distance)

                # part = math.sin(math.pi*part/2) ** 2

                alpha = int(part * self.halo_power)
                halo_surface.set_alpha(alpha)
                sprite.blit(halo_surface, (i, j))

        sprite.blit(text_surface, (halo_w, halo_h))
        return sprite
