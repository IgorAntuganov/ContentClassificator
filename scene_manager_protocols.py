from __future__ import annotations
import pygame
from typing import Protocol
from abc import abstractmethod
from UI_abstracts import MouseWheelState
from commands import BaseCommand
from UI_element import MetaUIElement


class CommandHandlerProtocol(Protocol):
    @property
    @abstractmethod
    def command_type(self):
        pass

    def handle(self, command: BaseCommand, scene: SceneProtocol):
        pass

    def handler_func(self, command: BaseCommand, scene: SceneProtocol):
        pass


class CommandHandlerFamilyProtocol(Protocol):
    @property
    @abstractmethod
    def command_type(self):
        pass

    def handle(self, command: BaseCommand, scene: SceneProtocol):
        pass

    def handler_func(self, command: BaseCommand, scene: SceneProtocol):
        pass


class ManagerProtocol(Protocol):
    def set_scene(self, scene: SceneProtocol):
        pass

    def register(self, handler: CommandHandlerProtocol):
        pass

    def register_family(self, family_handler: CommandHandlerFamilyProtocol):
        pass

    def handle_command(self, command):
        pass

    def handle_commands(self, commands_pool):
        pass

    def filter_handleable(self, commands_lst: list[BaseCommand]) -> list[BaseCommand]:
        pass

    def filter_non_handleable(self, commands_lst: list[BaseCommand]) -> list[BaseCommand]:
        pass


class SceneProtocol(Protocol):
    name: str = 'Protocol scene'

    def set_focused_element(self, element: MetaUIElement):
        pass

    def get_focused_element(self) -> MetaUIElement | None:
        pass

    def clear_focused_element(self):
        pass

    def handle_events(self) -> list[BaseCommand]:
        pass

    @staticmethod
    def get_ctrl_alt_shift_array() -> tuple[bool, bool, bool]:
        pass

    @staticmethod
    def update_mouse_wheel_state(mws: MouseWheelState, event: pygame.event.Event) -> MouseWheelState:
        pass

    def draw_elements(self, screen: pygame.Surface):
        pass
