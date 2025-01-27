from abc import ABC, abstractmethod
import pygame
import os
import json

from constants.configs import MouseConfig
from commands.abstract_commands import base_command_alias
from UI_elements.abstract_element import AbstractUIElement


class WithPrivateRect(ABC):
    def __init__(self, position: tuple[int, int], size: tuple[int, int]):
        self.position = position
        self.size = size
        self.__rect = pygame.Rect(position, size)

    def rect_collidepoint(self, point: tuple[int, int]) -> bool:
        return self.__rect.collidepoint(*point)

    def __update_position_and_size(self):
        self.position = self.__rect.topleft
        self.size = self.__rect.size

    def get_rect(self) -> pygame.Rect:
        return self.__rect

    def get_rect_topleft(self) -> tuple[int, int]:
        return self.__rect.topleft

    def get_size(self) -> tuple[int, int]:
        return self.__rect.size

    def set_rect(self, rect: pygame.Rect):
        self.__rect = rect
        self.__update_position_and_size()

    def set_top_left(self, top_left: tuple[int, int]):
        self.__rect.topleft = top_left
        self.__update_position_and_size()

    def set_size(self, size: tuple[int, int]):
        self.__rect.size = size
        self.__update_position_and_size()


class JSONadjustable(ABC):
    def __init__(self, path_to_json: str, **kwargs):
        """:param path_to_json: Path to save file
        :param kwargs: Dict with all values to adjust. Dict keys: 'var_name', values: var_value
        Example of usage: __init__(self, 'path_to_json', position=position, size=size)
        """
        self.path_to_json = path_to_json

        assert len(kwargs) > 0
        for k in kwargs.keys():
            if k not in self.__dict__:
                raise AssertionError(f'Something missing in __dict__: {k} NOT IN {self.__dict__}')

        if self._if_file_save_exists(path_to_json):
            adjusted_values_dct = self._load_adjusted_values_from_json()
            kwargs.update(adjusted_values_dct)
        self.adjusted_values = kwargs
        self.__dict__.update(kwargs)

    @classmethod
    def _if_file_save_exists(cls, path_to_json: str) -> bool:
        return os.path.exists(path_to_json)

    def _get_dict_for_json(self) -> dict:
        values_dct = {}
        for key in self.adjusted_values:
            values_dct[key] = self.__dict__[key]
        return values_dct

    def _load_adjusted_values_from_json(self) -> dict:
        with open(self.path_to_json, 'r') as file:
            adjusted_values_dict = json.load(file)
        return adjusted_values_dict

    def save_to_json(self):
        adjusted_values = self._get_dict_for_json()
        with open(self.path_to_json, 'w') as file:
            print('dumping', adjusted_values, self.path_to_json)
            json.dump(adjusted_values, file)


class MouseHandler(ABC):
    @abstractmethod
    def handle_mouse(self, mouse_config: MouseConfig) -> list[base_command_alias]:
        pass


class UIElement(AbstractUIElement, MouseHandler, ABC):
    pass
