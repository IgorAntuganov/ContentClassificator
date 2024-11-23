import pygame
from fonts import fonts_dict
from UI_abstracts import JSONable, Draggable, Drawable
from states import MouseWheelState


class SimpleText(JSONable, Draggable, Drawable):
    @classmethod
    def create_sprite(cls, font, text, color) -> pygame.Surface:
        text_surface = font.render(text, True, color)
        return text_surface

    def __init__(self, text,  path_to_json: str,
                 font_key=None,
                 color: tuple[int, int, int] = (200, 200, 200),
                 position=(250, 50)):
        JSONable.__init__(self, path_to_json=path_to_json)
        if JSONable.if_file_save_exists(path_to_json):
            position = self.get_list_of_adjusted_values()

        assert font_key in fonts_dict
        font = fonts_dict[font_key]
        self.sprite = self.create_sprite(font, text, color)

        self.rect = self.sprite.get_rect(center=position)
        Draggable.__init__(self, self.rect)

    def handle_event(self, mouse_position,
                     mouse_pressed,
                     mouse_wheel_state: MouseWheelState | None = None,
                     ctrl_alt_shift_array: tuple[bool, bool, bool] = (False, False, False)):
        if not self.rect.collidepoint(mouse_position) or not mouse_pressed[2]:  # RMB
            self.dragging = False
        else:
            self.handle_dragging(mouse_position)

    def get_dict_for_json(self) -> dict:
        return {'position': self.rect.center}

    def get_list_of_adjusted_values(self) -> list:
        adjusted_dict = self.load_adjusted_values_from_json()
        return adjusted_dict['position']

    def draw(self, screen: pygame.Surface):
        screen.blit(self.sprite, self.rect)
