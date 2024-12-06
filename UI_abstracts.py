from abc import ABC, abstractmethod
from dataclasses import dataclass
import pygame
import os
import json
from constants import SCREEN_RECT, BUTTON_SCREEN_COLLISION_DEFLATION
from states import MouseWheelState
from commands import BaseCommand
from UI_element import MetaUIElement


class WithPrivateRect(ABC):
    def __init__(self, position: tuple[int, int], size: tuple[int, int]):
        self.position = position
        self.size = size
        self.__rect = pygame.Rect(position, size)

    def rect_collidepoint(self, point: tuple[int, int]) -> bool:
        return self.__rect.collidepoint(*point)

    def update_position_and_size(self):
        self.position = self.__rect.topleft
        self.size = self.__rect.size

    def get_rect(self) -> pygame.Rect:
        return self.__rect

    def get_rect_topleft(self) -> tuple[int, int]:
        return tuple(self.__rect.topleft)

    def get_size(self) -> tuple[int, int]:
        return self.__rect.size

    def set_rect(self, rect: pygame.Rect):
        self.__rect = rect
        self.update_position_and_size()

    def set_top_left(self, top_left: tuple[int, int]):
        self.__rect.topleft = top_left
        self.update_position_and_size()

    def set_size(self, size: tuple[int, int]):
        self.__rect.size = size
        self.update_position_and_size()


class JSONadjustable(ABC):
    def __init__(self, path_to_json: str, **kwargs):
        """:param path_to_json: Path to save file
        :param kwargs: Dict with all values to adjust. Dict keys: 'var_name', values: var_value
        Example of usage: __init__(self, 'path_to_json', position=position, size=size)
        """
        self.path_to_json = path_to_json

        assert len(kwargs) > 0
        for k in kwargs.keys():
            assert k in self.__dict__

        if self.if_file_save_exists(path_to_json):
            adjusted_values_dct = self.load_adjusted_values_from_json()
            kwargs.update(adjusted_values_dct)
        self.adjusted_values = kwargs
        self.__dict__.update(kwargs)

    @classmethod
    def if_file_save_exists(cls, path_to_json: str) -> bool:
        return os.path.exists(path_to_json)

    def get_dict_for_json(self) -> dict:
        values_dct = {}
        for key in self.adjusted_values:
            values_dct[key] = self.__dict__[key]
        return values_dct

    def save_to_json(self):
        adjusted_values = self.get_dict_for_json()
        with open(self.path_to_json, 'w') as file:
            json.dump(adjusted_values, file)

    def load_adjusted_values_from_json(self) -> dict:
        with open(self.path_to_json, 'r') as file:
            adjusted_values_dict = json.load(file)
        return adjusted_values_dict


@dataclass
class MouseConfig:
    mouse_position: tuple[int, int]
    mouse_pressed: tuple[bool, bool, bool]
    mouse_wheel_state: MouseWheelState
    ctrl_alt_shift_array: tuple[bool, bool, bool]


class MouseHandler(ABC):
    @abstractmethod
    def handle_mouse(self, mouse_config: MouseConfig) -> list[BaseCommand]:
        pass


class BaseUIElement(MetaUIElement, MouseHandler, ABC):
    pass


class Draggable(WithPrivateRect, BaseUIElement, ABC):
    def __init__(self, position: tuple[int, int], size: tuple[int, int]):
        self.position = position
        WithPrivateRect.__init__(self, position, size)
        self.dragging = False
        self.dragging_start_mouse = None
        self.dragging_start_top_left = None

    def handle_dragging(self, config: MouseConfig):
        mouse_on_element = self.rect_collidepoint(config.mouse_position)
        rmb_pressed = config.mouse_pressed[2]
        if not self.dragging and mouse_on_element and rmb_pressed:
            self.dragging = True
            self.dragging_start_mouse = config.mouse_position
            self.dragging_start_top_left = self.get_rect_topleft()
        elif self.dragging and rmb_pressed:
            last_position = self.get_rect_topleft()
            offset_x = config.mouse_position[0] - self.dragging_start_mouse[0]
            offset_y = config.mouse_position[1] - self.dragging_start_mouse[1]
            x = self.dragging_start_top_left[0] + offset_x
            y = self.dragging_start_top_left[1] + offset_y
            self.set_top_left((x, y))
            rect = self.get_rect()
            if not SCREEN_RECT.contains(rect.inflate(*BUTTON_SCREEN_COLLISION_DEFLATION)):
                self.dragging = False
                self.set_top_left(last_position)
        elif self.dragging:
            self.dragging = False


class Resizable(WithPrivateRect, BaseUIElement, ABC):
    @abstractmethod
    def recreate_sprites_after_resizing(self):
        pass

    def handle_size_changing(self, ctrl_alt_shift_array, mouse_wheel_state):
        sign = mouse_wheel_state.value
        if ctrl_alt_shift_array[2]:
            value = sign
        else:
            value = sign * 5

        curr_size = self.get_size()
        new_width, new_height = curr_size
        if ctrl_alt_shift_array[0]:
            new_width += value
        if ctrl_alt_shift_array[1]:
            new_height += value

        self.set_size((new_width, new_height))
        self.recreate_sprites_after_resizing()


class OnlyDraggableElement(JSONadjustable, Draggable, ABC):
    pass


class DraggableAndResizableElement(Resizable, OnlyDraggableElement, ABC):
    pass
