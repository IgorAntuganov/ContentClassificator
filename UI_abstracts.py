from abc import ABC, abstractmethod
import pygame
import os
import json
from constants import SCREEN_RECT, BUTTON_SCREEN_COLLISION_DEFLATION
from states import MouseWheelState


class JSONable(ABC):
    def __init__(self, path_to_json: str):
        self.path_to_json = path_to_json

    @classmethod
    def if_file_save_exists(cls, path_to_json: str) -> bool:
        return os.path.exists(path_to_json)

    @abstractmethod
    def get_dict_for_json(self) -> dict:
        pass

    @abstractmethod
    def get_list_of_adjusted_values(self) -> list:
        pass

    def save_to_json(self):
        adjusted_values = self.get_dict_for_json()
        with open(self.path_to_json, 'w') as file:
            json.dump(adjusted_values, file)

    def load_adjusted_values_from_json(self) -> dict:
        with open(self.path_to_json, 'r') as file:
            adjusted_values_dict = json.load(file)
        return adjusted_values_dict


class Draggable(ABC):
    def __init__(self, rect: pygame.Rect):
        self.rect = rect
        self.dragging = False
        self.dragging_start_mouse = None
        self.dragging_start_top_left = None

    def handle_dragging(self, mouse_position):
        if not self.dragging:
            self.dragging = True
            self.dragging_start_mouse = mouse_position
            self.dragging_start_top_left = self.rect.topleft
        else:
            last_position = self.rect.topleft
            offset_x = mouse_position[0] - self.dragging_start_mouse[0]
            offset_y = mouse_position[1] - self.dragging_start_mouse[1]
            self.rect.x = self.dragging_start_top_left[0] + offset_x
            self.rect.y = self.dragging_start_top_left[1] + offset_y
            if not SCREEN_RECT.contains(self.rect.inflate(*BUTTON_SCREEN_COLLISION_DEFLATION)):
                self.dragging = False
                self.rect.topleft = last_position

    @abstractmethod
    def handle_event(self, mouse_position,
                     mouse_pressed,
                     mouse_wheel_state: MouseWheelState | None = None,
                     ctrl_alt_shift_array: tuple[bool, bool, bool] = (False, False, False)):
        pass


class Resizable(ABC):
    @abstractmethod
    def get_rect(self) -> pygame.Rect:
        pass

    @abstractmethod
    def set_size(self, size: tuple[int, int]):
        pass

    @abstractmethod
    def get_size(self) -> tuple[int, int]:
        pass

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


class Drawable(ABC):
    @abstractmethod
    def draw(self, screen: pygame.Surface):
        pass
