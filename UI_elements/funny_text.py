from abc import abstractmethod, ABC
from dataclasses import dataclass
import constants.constants as cnst
import pygame

from constants.styles import key_to_font
from constants.configs import EventConfig
from UI_elements.manual_adjusting import Draggable
from commands.abstract_commands import CommandList


@dataclass
class TextConfig:
    text: str
    font_key: str | int | None = None
    color: tuple[int, int, int] = cnst.STANDARD_UI_BRIGHT


class SimpleText(Draggable, ABC):
    def __init__(self, config: TextConfig):
        super().__init__()

        self.font = key_to_font(config.font_key)
        self.text = config.text
        self.color = config.color
        self.sprite = pygame.Surface((10, 10))
        self._draw_sprites()
        self._savable_config.size = self.sprite.get_size()

    @abstractmethod
    def create_sprite(self) -> pygame.Surface:
        pass

    def _draw_sprites(self):
        self.sprite = self.create_sprite()

    def handle_events(self, config: EventConfig) -> CommandList:
        return self.handle_dragging(config)

    def get_sprite(self) -> pygame.Surface:
        return self.sprite


@dataclass
class ShadowedTextConfig(TextConfig):
    shadow_color: tuple[int, int, int] = cnst.STANDARD_UI_RED
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
                if i % 2 != 0 or j % 2 != 0:
                    continue
                distance = ((halo_w - i)**2 + (halo_h - j)**2)**0.5
                part = 1 - (distance / max_distance)
                alpha = int(part * self.halo_power)
                halo_surface.set_alpha(alpha)
                sprite.blit(halo_surface, (i, j))

        sprite.blit(text_surface, (halo_w, halo_h))
        return sprite
