from abc import abstractmethod, ABC
import pygame
from constants.configs import MouseConfig
from commands.abstract_commands import base_command_alias


class AbstractUIElement(ABC):
    """Base UI class"""
    @abstractmethod
    def draw(self, screen: pygame.Surface):
        pass

    @abstractmethod
    def handle_mouse(self, config: MouseConfig) -> list[base_command_alias]:
        pass
