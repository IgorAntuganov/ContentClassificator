from abc import abstractmethod, ABC
import pygame


class UIElement(ABC):
    """Base UI class"""
    @abstractmethod
    def draw(self, screen: pygame.Surface):
        pass
