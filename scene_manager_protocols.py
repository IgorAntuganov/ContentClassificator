import pygame
from typing import Protocol
from UI_abstracts import MouseWheelState
from commands import BaseCommand
from UI_element import MetaUIElement

class ManagerProtocol(Protocol):
    pass


class SceneProtocol(Protocol):
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
