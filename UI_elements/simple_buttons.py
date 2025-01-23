from dataclasses import dataclass
from abc import abstractmethod
import pygame

from constants.enums import QuadButtonState, MouseWheelState, DraggingState
from constants.configs import MouseConfig

from commands.abstract_commands import AbstractCommand
from commands.dragging_commands import EndDragging
from commands.hover_commands import *

import constants.constants as cnst
from constants.fonts import fonts_dict
from constants.color_schemes import buttons_color_schemes_dict

from UI_elements.manual_adjusting import DraggableAndResizableElement


@dataclass
class ButtonConfig:
    text: str
    command: AbstractCommand
    path_to_json: str
    position: tuple[int, int] = cnst.STANDARD_UI_POSITION
    size: tuple[int, int] = cnst.STANDARD_UI_SIZE
    colors_key: str | int | None = None
    font_key: str | int | None = None


class ABCQuadStateButton(DraggableAndResizableElement, ABC):
    def __init__(self, config: ButtonConfig):
        self.position = config.position
        self.size = config.size
        super().__init__(config.path_to_json, self.position, self.size)

        self.text = config.text
        self.command = config.command

        assert config.font_key in fonts_dict
        self.font = fonts_dict[config.font_key]
        assert config.colors_key in buttons_color_schemes_dict
        self.colors = buttons_color_schemes_dict[config.colors_key]

        self.current_state = QuadButtonState.NORMAL
        self.sprites = self.create_all_sprites()

    def recreate_sprites_after_resizing(self):
        self.sprites = self.create_all_sprites()

    @abstractmethod
    def create_all_sprites(self) -> dict[QuadButtonState, pygame.Surface]:
        pass

    def draw(self, screen: pygame.Surface):
        screen.blit(self.sprites[self.current_state], self.get_rect())

    @staticmethod
    def is_size_changing(mouse_config: MouseConfig) -> bool:
        # noinspection PyPep8Naming
        RMB_pressed = mouse_config.mouse_pressed[2]
        mouse_wheel_nan = mouse_config.mouse_wheel_state is not None
        mouse_wheel_active = mouse_config.mouse_wheel_state != MouseWheelState.INACTIVE
        return RMB_pressed and mouse_wheel_nan and mouse_wheel_active

    def is_inactive(self, mouse_config: MouseConfig) -> bool:
        dragging_offed = not self.is_dragging
        not_pressed = self.current_state not in (QuadButtonState.PRESSED, QuadButtonState.PRESSED_OUTSIDE)
        not_collide = not self.rect_collidepoint(mouse_config.mouse_position)
        return dragging_offed and not_pressed and not_collide

    def handle_inactive(self) -> list[AbstractCommand]:
        commands_lst: list[AbstractCommand] = []
        if self.dragging == DraggingState.ENDING:
            commands_lst.append(EndDragging())
        if self.current_state in (QuadButtonState.PRESSED,
                                  QuadButtonState.PRESSED_OUTSIDE,
                                  QuadButtonState.HOVER):
            commands_lst.append(EndHover())

        self.current_state = QuadButtonState.NORMAL
        return commands_lst

    def handle_pressed(self, commands_lst: list[AbstractCommand], mouse_config: MouseConfig) -> list[AbstractCommand]:
        if self.current_state == QuadButtonState.NORMAL:
            commands_lst.append(StartHover())
        else:
            commands_lst.append(KeepHover())

        if self.rect_collidepoint(mouse_config.mouse_position):
            self.current_state = QuadButtonState.PRESSED
        else:
            self.current_state = QuadButtonState.PRESSED_OUTSIDE

        return commands_lst

    def handle_mouse(self, mouse_config: MouseConfig) -> list[AbstractCommand]:
        commands_lst: list[AbstractCommand] = []

        if self.is_inactive(mouse_config):
            return self.handle_inactive()

        dragging_commands = self.handle_dragging(mouse_config)

        if self.is_size_changing(mouse_config):
            self.handle_size_changing(mouse_config.ctrl_alt_shift_array,
                                      mouse_config.mouse_wheel_state)

        # LMB pressed
        if len(dragging_commands) == 0 and mouse_config.mouse_pressed[0]:
            return self.handle_pressed(commands_lst, mouse_config)

        # LMB unpressed (legitimate click)
        if self.current_state == QuadButtonState.PRESSED:
            commands_lst.append(self.command)

        if len(dragging_commands) > 0:
            if self.current_state != QuadButtonState.NORMAL:
                commands_lst.append(EndHover())
            self.current_state = QuadButtonState.NORMAL
        elif self.rect_collidepoint(mouse_config.mouse_position):
            if self.current_state == QuadButtonState.NORMAL:
                commands_lst.append(StartHover())
            else:
                commands_lst.append(KeepHover())
            self.current_state = QuadButtonState.HOVER
        else:
            self.current_state = QuadButtonState.NORMAL
            commands_lst.append(EndHover())

        commands_lst.extend(dragging_commands)
        return commands_lst


class SimpleButton(ABCQuadStateButton):
    def __init__(self, config: ButtonConfig, border_radius=cnst.SimpleButton_BORDER_RADIUS):
        self.border_radius = border_radius
        ABCQuadStateButton.__init__(self, config)

    def create_all_sprites(self) -> dict[QuadButtonState, pygame.Surface]:
        sprites = {
            QuadButtonState.NORMAL: self._create_sprite_with_deflation(
                self.colors[QuadButtonState.NORMAL],
                deflation=cnst.NORMAL_BUTTON_SPRITE_DEFLATION,
                text_descent=0
            ),
            QuadButtonState.HOVER: self._create_sprite_with_deflation(
                self.colors[QuadButtonState.HOVER],
                deflation=(0, 0),
                text_descent=0
            ),
            QuadButtonState.PRESSED: self._create_sprite_with_deflation(
                self.colors[QuadButtonState.PRESSED],
                deflation=cnst.ACTIVE_BUTTON_SPRITE_DEFLATION,
                text_descent=cnst.ACTIVE_BUTTON_TEXT_DESCENT
            ),
            QuadButtonState.PRESSED_OUTSIDE: self._create_sprite_with_deflation(
                self.colors[QuadButtonState.PRESSED_OUTSIDE],
                deflation=cnst.ACTIVE_BUTTON_SPRITE_DEFLATION,
                text_descent=cnst.ACTIVE_BUTTON_TEXT_DESCENT
            )
        }
        return sprites

    def _create_sprite_with_deflation(self, color, deflation, text_descent):
        sprite = pygame.Surface(self.get_size(), pygame.SRCALPHA)

        rect = sprite.get_rect().inflate(deflation)
        rect.move_ip(0, -deflation[1]//2)
        smaller_rect = rect.inflate(cnst.BUTTON_OUTLINE_CREATING_DEFLATION)
        multi = cnst.OUTLINE_DARKENING_COEFFICIENT
        darker_color = list(map(lambda x: max(0, min(255, x*multi)), color))

        pygame.draw.rect(sprite, darker_color, rect, border_radius=self.border_radius)
        pygame.draw.rect(sprite, color, smaller_rect, border_radius=self.border_radius)

        text_surface = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=sprite.get_rect().center)
        text_rect.move_ip(0, text_descent)
        sprite.blit(text_surface, text_rect)
        return sprite
