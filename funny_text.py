from dataclasses import dataclass
import constants as cnst
import pygame
from fonts import fonts_dict
from UI_abstracts import JSONadjustable, Draggable, OnlyDraggableElement, MouseConfig
from commands.command_classes import BaseCommand


@dataclass
class TextConfig:
    text: str
    path_to_json: str
    font_key: str | int | None = None
    color: tuple[int, int, int] = cnst.STANDARD_UI_BRIGHT
    position: tuple[int, int] = cnst.STANDARD_UI_POSITION


class SimpleText(OnlyDraggableElement):
    def __init__(self, config: TextConfig):
        self.position = config.position
        JSONadjustable.__init__(self, config.path_to_json, position=config.position)

        assert config.font_key in fonts_dict
        self.font = fonts_dict[config.font_key]
        self.text = config.text
        self.color = config.color
        self.sprite = self.create_sprite()

        Draggable.__init__(self, self.position, self.sprite.get_size())

    def create_sprite(self) -> pygame.Surface:
        text_surface = self.font.render(self.text, True, self.color)
        return text_surface

    def handle_mouse(self, config: MouseConfig) -> list[BaseCommand]:
        return self.handle_dragging(config)

    def draw(self, screen: pygame.Surface):
        screen.blit(self.sprite, self.get_rect())


@dataclass
class ShadowedTextConfig(TextConfig):
    shadow_color: tuple[int, int, int] = cnst.STANDARD_UI_DARK
    shadow_offset: tuple[int, int] = cnst.SHADOW_TEXT_OFFSET


class ShadowedText(SimpleText):
    def __init__(self, config: ShadowedTextConfig):
        self.shadow_color = config.shadow_color
        self.shadow_offset = config.shadow_offset
        super().__init__(config)

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


@dataclass
class OutlinedTextConfig(TextConfig):
    outline_color: tuple[int, int, int] = cnst.STANDARD_UI_RED
    outline_extent: tuple[int, int] = cnst.OUTLINE_EXTENT


class OutlinedText(SimpleText):
    def __init__(self, config: OutlinedTextConfig):
        self.outline_color = config.outline_color
        self.outline_extent = config.outline_extent
        super().__init__(config)

    def create_sprite(self) -> pygame.Surface:
        text_surface = self.font.render(self.text, True, self.color)
        outline_surface = self.font.render(self.text, True, self.outline_color)

        width, height = text_surface.get_rect().size
        halo_w, halo_h = self.outline_extent
        width += halo_w * 2
        height += halo_h * 2
        sprite = pygame.Surface((width, height), pygame.SRCALPHA)

        for i in range(halo_w * 2 + 1):
            for j in range(halo_h * 2 + 1):
                sprite.blit(outline_surface, (i, j))
        sprite.blit(text_surface, (halo_w, halo_h))
        return sprite


@dataclass
class HaloTextConfig(TextConfig):
    halo_color: tuple[int, int, int] = cnst.STANDARD_UI_RED
    halo_extent: tuple[int, int] = cnst.HALO_EXTENT
    halo_power: int = cnst.HALO_POWER


class HaloText(SimpleText):
    def __init__(self, config: HaloTextConfig):
        self.halo_color = config.halo_color
        self.halo_extent = config.halo_extent
        self.halo_power = config.halo_power
        super().__init__(config)

    def create_sprite(self) -> pygame.Surface:
        text_surface = self.font.render(self.text, True, self.color)
        halo_surface = self.font.render(self.text, True, self.halo_color)

        width, height = text_surface.get_rect().size
        halo_w, halo_h = self.halo_extent
        width += halo_w * 2
        height += halo_h * 2
        sprite = pygame.Surface((width, height), pygame.SRCALPHA)

        max_distance = (halo_w**2 + halo_h**2)**0.5
        for i in range(halo_w * 2 + 1):
            for j in range(halo_h * 2 + 1):
                distance = ((halo_w - i)**2 + (halo_h - j)**2)**0.5
                part = 1 - (distance / max_distance)
                alpha = int(part * self.halo_power)
                halo_surface.set_alpha(alpha)
                sprite.blit(halo_surface, (i, j))

        sprite.blit(text_surface, (halo_w, halo_h))
        return sprite
