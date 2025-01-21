from __future__ import annotations
import pygame
from typing import Protocol
from abc import abstractmethod

from constants.enums import MouseWheelState, TargetPriority
from UI_elements.abstract_element import AbstractUIElement
from cursor_manager import CursorManager


class BaseCommandProtocol(Protocol):
    @property
    @abstractmethod
    def text(self):
        pass


class SceneProtocol(Protocol):
    name: str = 'Protocol scene'

    def set_target(self, element: AbstractUIElement, priority: TargetPriority):
        pass

    def keep_target(self, element: AbstractUIElement, priority: TargetPriority):
        pass

    def clear_target(self, element: AbstractUIElement, priority: TargetPriority):
        pass

    def get_cursor_manager(self) -> CursorManager:
        pass

    def get_elements_manager(self):  # can't type hint output
        pass

    def handle_events(self) -> list[BaseCommandProtocol]:
        pass

    @staticmethod
    def get_ctrl_alt_shift_array() -> tuple[bool, bool, bool]:
        pass

    @staticmethod
    def update_mouse_wheel_state(mws: MouseWheelState, event: pygame.event.Event) -> MouseWheelState:
        pass

    def draw_elements(self, screen: pygame.Surface):
        pass

    def save_elements(self):
        pass
