from dataclasses import dataclass
from abc import ABC, abstractmethod
import pygame
from states import TripleButtonState, MouseWheelState
from commands import TextCommand
import constants as cnst
from fonts import fonts_dict
from color_schemes import buttons_color_schemes_dict
from UI_abstracts import JSONadjustable, Draggable, DraggableAndResizableElement, EventConfig


@dataclass
class ButtonConfig:
    text: str
    command: TextCommand
    path_to_json: str
    position: tuple[int, int] = cnst.STANDARD_UI_POSITION
    size: tuple[int, int] = cnst.STANDARD_UI_SIZE
    colors_key: str | int = None
    font_key: str | int = None


class ABCTripleStateButton(DraggableAndResizableElement, ABC):
    def __init__(self, config: ButtonConfig):
        self.position = config.position
        self.size = config.size
        JSONadjustable.__init__(self, config.path_to_json, position=config.position, size=config.size)
        Draggable.__init__(self, self.position, self.size)

        self.text = config.text
        self.command = config.command

        assert config.font_key in fonts_dict
        self.font = fonts_dict[config.font_key]
        assert config.colors_key in buttons_color_schemes_dict
        self.colors = buttons_color_schemes_dict[config.colors_key]

        self.current_state = TripleButtonState.NORMAL
        self.sprites = self.create_all_sprites()

    def recreate_sprites_after_resizing(self):
        self.sprites = self.create_all_sprites()

    @abstractmethod
    def create_all_sprites(self) -> dict[TripleButtonState:pygame.Surface]:
        pass

    def draw(self, screen: pygame.Surface):
        screen.blit(self.sprites[self.current_state], self.get_rect())

    def handle_event(self, config: EventConfig) -> None | TextCommand:
        if not self.rect_collidepoint(config.mouse_position):
            self.current_state = TripleButtonState.NORMAL
            self.dragging = False
            return

        unpressed = False
        if config.mouse_pressed[0]:  # LMB
            self.current_state = TripleButtonState.ACTIVE
        elif config.mouse_pressed[2]:  # RMB
            self.handle_dragging(config.mouse_position)
            if (config.mouse_wheel_state is not None) and \
                    (config.mouse_wheel_state != MouseWheelState.INACTIVE):
                self.handle_size_changing(config.ctrl_alt_shift_array, config.mouse_wheel_state)
        else:
            if self.current_state == TripleButtonState.ACTIVE:
                unpressed = True
            self.current_state = TripleButtonState.HOVER
            self.dragging = False

        if unpressed:
            return self.command


class SimpleButton(ABCTripleStateButton):
    def __init__(self, config: ButtonConfig, border_radius=7):
        self.border_radius = border_radius
        ABCTripleStateButton.__init__(self, config)

    def create_all_sprites(self) -> dict[TripleButtonState:pygame.Surface]:
        sprites = {
            TripleButtonState.NORMAL: self._create_sprite_with_deflation(
                self.colors[TripleButtonState.NORMAL],
                deflation=cnst.NORMAL_BUTTON_SPRITE_DEFLATION
            ),
            TripleButtonState.HOVER: self._create_sprite_with_deflation(
                self.colors[TripleButtonState.HOVER],
                deflation=(0, 0)
            ),
            TripleButtonState.ACTIVE: self._create_sprite_with_deflation(
                self.colors[TripleButtonState.ACTIVE],
                deflation=cnst.ACTIVE_BUTTON_SPRITE_DEFLATION
            )
        }
        return sprites

    def _create_sprite_with_deflation(self, color, deflation):
        sprite = pygame.Surface(self.get_size(), pygame.SRCALPHA)
        pygame.draw.rect(sprite, color, sprite.get_rect().inflate(deflation), border_radius=self.border_radius)
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=sprite.get_rect().center)
        sprite.blit(text_surface, text_rect)
        return sprite


class CoolRectButton(ABCTripleStateButton):
    def __init__(self, config: ButtonConfig):
        ABCTripleStateButton.__init__(self, config)

    def create_all_sprites(self) -> dict[TripleButtonState:pygame.Surface]:
        pass
