from abc import abstractmethod, ABC
import pygame


class MetaUIElement(ABC):
    """Base UI class"""
    @abstractmethod
    def draw(self, screen: pygame.Surface):
        pass

    @abstractmethod
    def handle_mouse(self, *args, **kwargs):
        pass
