import pygame

from commands.abstract_commands import CommandList
from constants.styles import key_to_font
from constants.configs import EventConfig
from UI_elements.manual_adjusting import Resizable


def generate_element_name(folder_path: str) -> str:
    nice_path = folder_path.replace('/', '_').replace('\\', '_').replace(':', '_')
    return f"FolderIcon_{nice_path}"


class FolderIcon(Resizable):
    def __init__(self, _path: str):
        super().__init__()
        self._path = _path
        self.font = key_to_font(None)

    def get_sprite(self) -> pygame.Surface:
        sizes = self.get_savable_config().size
        text = self.font.render(self._path, 1, (200, 200, 200))
        sprite = pygame.Surface(sizes)
        sprite.blit(text, (0, 0))
        return sprite

    def handle_events(self, config: EventConfig) -> CommandList:
        return self.handle_dragging(config)

    def _draw_sprites(self):
        pass
