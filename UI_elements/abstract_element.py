from abc import abstractmethod, ABC
import pygame
from constants.configs import EventConfig
from commands.abstract_commands import CommandList


class UIElement(ABC):
    """Base UI class"""
    @abstractmethod
    def draw(self, screen: pygame.Surface):
        pass

    @abstractmethod
    def handle_events(self, config: EventConfig) -> CommandList:
        pass
