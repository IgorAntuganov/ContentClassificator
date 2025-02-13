from abc import abstractmethod, ABC
import pygame

from constants.configs import EventConfig, SavableConfig
from commands.abstract_commands import CommandList


class UIElement(ABC):
    def __init__(self):
        self._savable_config: SavableConfig = SavableConfig()

    def draw(self, screen: pygame.Surface):
        screen.blit(self.get_sprite(), self.get_rect())

    @abstractmethod
    def get_sprite(self) -> pygame.Surface:
        pass

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self._savable_config.position, self._savable_config.size)

    @abstractmethod
    def handle_events(self, config: EventConfig) -> CommandList:
        pass

    def get_savable_config(self) -> SavableConfig:
        return self._savable_config

    def set_savable_config(self, config: SavableConfig):
        self._savable_config = config
        self._draw_sprites()

    @abstractmethod
    def _draw_sprites(self):
        pass
