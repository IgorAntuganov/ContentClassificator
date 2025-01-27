from dataclasses import dataclass
import os
import pygame

from constants.configs import MouseConfig
from UI_elements.manual_adjusting import DraggableAndResizableElement
from commands.abstract_commands import base_command_alias
from constants.constants import IMAGES_FORMATS, IMAGE_SEQUENCE_BACKGROUND


def _images_paths_from_folder(path_to_folder: str | bytes) -> list[str]:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    images_folder_path = os.path.join(project_root, str(path_to_folder))
    paths = []
    for f in os.listdir(images_folder_path):
        if f.endswith(IMAGES_FORMATS):
            paths.append(os.path.join(images_folder_path, f))
    return paths


def _load_and_scale_image(image_path: str | bytes, max_width: int, max_height: int) -> pygame.Surface:
    image = pygame.image.load(image_path)
    orig_width, orig_height = image.get_size()

    scale_factor = min(max_width / orig_width, max_height / orig_height)
    new_size = (int(orig_width * scale_factor), int(orig_height * scale_factor))

    return pygame.transform.smoothscale(image, new_size)


@dataclass
class ImageSeqConfig:
    path_to_image_folder: str
    path_to_json: str
    position: tuple[int, int]
    size: tuple[int, int]


class ImageSequence(DraggableAndResizableElement):
    def __init__(self, image_seq_config: ImageSeqConfig):
        self.position = image_seq_config.position
        self.size = image_seq_config.size
        super().__init__(image_seq_config.path_to_json, self.position, self.size)

        self._images_folder_path = image_seq_config.path_to_image_folder
        assert os.path.isdir(self._images_folder_path)
        self._images_paths = _images_paths_from_folder(image_seq_config.path_to_image_folder)
        if len(self._images_paths) < 1:
            raise AssertionError('Zero images in image folder')

        self._image_index = 0

        self._sprite = pygame.Surface(self.size)
        self._draw_sprite()


    def next_image(self):
        assert self._image_index < self.get_images_count() - 1
        self._image_index += 1
        self._draw_sprite()

    def set_image_index(self, ind: int):
        assert 0 <= ind < self.get_images_count()
        self._image_index = ind

    def get_image_index(self) -> int:
        return self._image_index

    def get_images_count(self) -> int:
        return len(self._images_paths)


    def _draw_sprite(self):
        self._sprite.fill(IMAGE_SEQUENCE_BACKGROUND)
        self._load_and_blit_image()

    def _load_and_blit_image(self):
        image_path = self._images_paths[self._image_index]
        image = _load_and_scale_image(image_path, *self.size)
        blit_rect = image.get_rect(center=self._sprite.get_rect().center)
        self._sprite.blit(image, blit_rect)


    def draw(self, screen: pygame.Surface):
        screen.blit(self._sprite, self.get_rect())

    def handle_mouse(self, config: MouseConfig) -> list[base_command_alias]:
        return self.handle_dragging(config)

    def recreate_sprites_after_resizing(self):
        self._sprite = pygame.Surface(self.size)
        self._draw_sprite()
