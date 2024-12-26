import pygame
import time
from dataclasses import dataclass
from typing import Generator

FRAME_TIME = .1  # in seconds

@dataclass
class MandelbrotConfig:
    size_rect: pygame.Rect = pygame.Rect((0, 0, 1024, 1024))
    coords_rect_left_top: tuple[float, float] = (-2, -1.5)
    coords_rect_size: tuple[float, float] = (3, 3)
    max_depth: int = 100


def get_pixel_size(config: MandelbrotConfig) -> tuple[float, float]:
    pixel_width = config.coords_rect_size[0] / config.size_rect.width
    pixel_height = config.coords_rect_size[1] / config.size_rect.height
    pixel_width = round(pixel_width, 15)
    pixel_height = round(pixel_height, 15)
    return pixel_width, pixel_height


def pixel_index_iterator(config: MandelbrotConfig) -> Generator[tuple[int, int], None, None]:
    for i in range(config.size_rect.width):
        for j in range(config.size_rect.height):
            yield i, j


def pixel_index_to_cords(config:     MandelbrotConfig,
                         ij_tuple:   tuple[int, int],
                         pixel_size: tuple[float, float]) -> tuple[float, float]:
    i, j = ij_tuple
    pixel_width, pixel_height = pixel_size

    left = config.coords_rect_left_top[0]
    top = config.coords_rect_left_top[1]
    x = left + pixel_width * i
    y = top + pixel_height * j

    if i == 0 and j == 0:
        print('first xy', x, y)
    if i == config.size_rect.width-1 and j == config.size_rect.height-1:
        print('last xy', x, y)
    return x, y


def mandelbrot_value(x: float, y: float, depth: int) -> int:
    z: complex
    c: complex
    z = c = x + 1j * y
    for k in range(depth):
        z = z ** 2 + c
        hypo_sqr = z.real ** 2 + z.imag ** 2
        if hypo_sqr > 4:
            return k
    return depth


def value_to_color(value: int, depth: int) -> tuple[int, int, int]:
    if value == depth:
        return 0, 0, 0
    color_value = 200 - value * 2
    return (color_value,) * 3

def update_screen(screen: pygame.Surface, image: pygame.Surface):
    screen.blit(image, (0, 0))
    pygame.display.flip()

def main(config: MandelbrotConfig):
    start = time.time()
    time_tick = time.time()
    screen = pygame.display.set_mode(config.size_rect.size)

    image = pygame.Surface(config.size_rect.size)
    pixel_size = get_pixel_size(config)
    for ij in pixel_index_iterator(config):
        x, y = pixel_index_to_cords(config, ij, pixel_size)
        value = mandelbrot_value(x, y, config.max_depth)
        color = value_to_color(value, config.max_depth)
        image.set_at(ij, color)

        if time.time() - time_tick > FRAME_TIME:
            [exit() for event in pygame.event.get() if event.type == pygame.QUIT]
            update_screen(screen, image)
            time_tick = time.time()

    update_screen(screen, image)
    print('Elapsed time:', round(time.time()-start, 10))

    while True:
        [exit() for event in pygame.event.get() if event.type == pygame.QUIT]


if __name__ == '__main__':
    main(MandelbrotConfig())
