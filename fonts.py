import pygame

fonts_dict: dict[str | int | None, pygame.font.Font] = {
    1: pygame.font.SysFont('Tahoma', 25),
    None: pygame.font.Font('fonts_test/test_font.ttf', 25)
}
