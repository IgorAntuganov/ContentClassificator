from dataclasses import dataclass
from abc import ABC, abstractmethod
import pygame
from states import TripleButtonState, MouseWheelState
import commands
import constants as cnst
from fonts import fonts_dict
from color_schemes import buttons_color_schemes_dict
from UI_abstracts import JSONadjustable, Draggable, DraggableAndResizableElement, MouseConfig


@dataclass
class ButtonConfig:
    text: str
    command: commands.BaseCommand
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

    def handle_mouse(self, mouse_config: MouseConfig) -> list[commands.BaseCommand]:
        already_dragging = self.dragging
        self.handle_dragging(mouse_config)

        if not self.rect_collidepoint(mouse_config.mouse_position):
            self.current_state = TripleButtonState.NORMAL
            return []

        unpressed = False
        commands_lst = []
        # LMB
        if mouse_config.mouse_pressed[0]:
            self.current_state = TripleButtonState.ACTIVE
        # RMB
        elif mouse_config.mouse_pressed[2]:
            if (mouse_config.mouse_wheel_state is not None) and \
                    (mouse_config.mouse_wheel_state != MouseWheelState.INACTIVE):
                self.handle_size_changing(mouse_config.ctrl_alt_shift_array, mouse_config.mouse_wheel_state)
        else:
            if self.current_state == TripleButtonState.ACTIVE:
                unpressed = True
            self.current_state = TripleButtonState.HOVER

        if unpressed:
            commands_lst.append(self.command)

        if self.dragging:
            if already_dragging:
                comm = commands.KeepFocus.set_element_association(self)
            else:
                comm = commands.StartFocus.set_element_association(self)
            commands_lst.append(comm)
        elif already_dragging:
            comm = commands.EndFocus.set_element_association(self)
            commands_lst.append(comm)
        return commands_lst


class SimpleButton(ABCTripleStateButton):
    def __init__(self, config: ButtonConfig, border_radius=7):
        self.border_radius = border_radius
        ABCTripleStateButton.__init__(self, config)

    def create_all_sprites(self) -> dict[TripleButtonState:pygame.Surface]:
        sprites = {
            TripleButtonState.NORMAL: self._create_sprite_with_deflation(
                self.colors[TripleButtonState.NORMAL],
                deflation=cnst.NORMAL_BUTTON_SPRITE_DEFLATION,
                text_descent=0
            ),
            TripleButtonState.HOVER: self._create_sprite_with_deflation(
                self.colors[TripleButtonState.HOVER],
                deflation=(0, 0),
                text_descent=0
            ),
            TripleButtonState.ACTIVE: self._create_sprite_with_deflation(
                self.colors[TripleButtonState.ACTIVE],
                deflation=cnst.ACTIVE_BUTTON_SPRITE_DEFLATION,
                text_descent=cnst.ACTIVE_BUTTON_TEXT_DESCENT
            )
        }
        return sprites

    def _create_sprite_with_deflation(self, color, deflation, text_descent):
        sprite = pygame.Surface(self.get_size(), pygame.SRCALPHA)
        pygame.draw.rect(sprite, color, sprite.get_rect().inflate(deflation), border_radius=self.border_radius)
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=sprite.get_rect().center)
        text_rect.move_ip(0, text_descent)
        sprite.blit(text_surface, text_rect)
        return sprite


class CoolRectButton(ABCTripleStateButton):
    def __init__(self, config: ButtonConfig):
        ABCTripleStateButton.__init__(self, config)

    def create_all_sprites(self) -> dict[TripleButtonState:pygame.Surface]:
        pass
