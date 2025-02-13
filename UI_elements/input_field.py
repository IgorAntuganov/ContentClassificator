from dataclasses import dataclass
import pygame

from constants.configs import EventConfig
from UI_elements.manual_adjusting import DraggableAndResizableElement
from commands.abstract_commands import CommandList


@dataclass
class InputFieldConfig:
    placeholder_text: str


class InputField(DraggableAndResizableElement):
    def __init__(self, config: InputFieldConfig):
        super().__init__()

        self.text: str = ''
        self.cursor_position: int = 0
        self.placeholder_text = config.placeholder_text

        self.sprite = pygame.Surface(self._savable_config.size)
        self._draw_sprites()

    def _draw_sprites(self):
        pass

    def recreate_sprites_after_resizing(self):
        self._draw_sprites()

    def get_sprite(self) -> pygame.Surface:
        return self.sprite

    def handle_events(self, config: EventConfig) -> CommandList:
        return self.handle_dragging(config)
