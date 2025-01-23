from abc import abstractmethod, ABC
import pygame
from constants.configs import MouseConfig


class AbstractUIElement(ABC):
    """Base UI class"""
    @abstractmethod
    def draw(self, screen: pygame.Surface):
        pass

    @abstractmethod
    def handle_mouse(self, config: MouseConfig):
        pass
