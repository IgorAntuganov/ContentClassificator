import pygame
import time
from dataclasses import dataclass
from typing import Generator

FRAME_TIME = .2  # in seconds

@dataclass
class MandelbrotConfig:
    rect_size: pygame.Rect = pygame.Rect((0, 0, 1280, 720))
    coords_rect_left_top: tuple[float, float] = (-4, -3)
    coords_rect_size: tuple[float, float] = (8, 6)
    max_depth: int = 32


def get_pixel_size(config: MandelbrotConfig) -> tuple[float, float]:
    pixel_width = config.coords_rect_size[0] / config.rect_size.width
    pixel_height = config.coords_rect_size[1] / config.rect_size.height
    pixel_width = round(pixel_width, 15)
    pixel_height = round(pixel_height, 15)
    return pixel_width, pixel_height


def pixel_index_iterator(config: MandelbrotConfig) -> Generator[tuple[int, int], None, None]:
    for i in range(config.rect_size.width):
        for j in range(config.rect_size.height):
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

    # if i == 0 and j == 0:
    #     print('first xy', x, y)
    # if i == config.rect_size.width-1 and j == config.rect_size.height-1:
    #     print('last xy', x, y)
    return x, y


def mandelbrot_value(x: float, y: float, depth: int, n: float) -> int:
    z: complex
    c: complex
    z = x + 1j * y
    if z == 0:
        return depth
    for k in range(depth):
        z = z ** n - z
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
    screen = pygame.display.set_mode(config.rect_size.size)

    image = pygame.Surface(config.rect_size.size)
    pixel_size = get_pixel_size(config)
    for k in range(-121, 121):
        print(f'\r{k}', end='')
        n = round(k/10, 1)
        for ij in pixel_index_iterator(config):
            x, y = pixel_index_to_cords(config, ij, pixel_size)
            try:
                value = mandelbrot_value(x, y, config.max_depth, n)
                color = value_to_color(value, config.max_depth)
            except ZeroDivisionError:
                color = (250, 0, 0)
            except OverflowError:
                color = (0, 250, 0)
            image.set_at(ij, color)

            if time.time() - time_tick > FRAME_TIME:
                [exit() for event in pygame.event.get() if event.type == pygame.QUIT]
                update_screen(screen, image)
                time_tick = time.time()
        file_index = k + 121
        pygame.image.save(image, f'image_folder2/{file_index}_({n}).png')

    update_screen(screen, image)
    print('Elapsed time:', round(time.time()-start, 10))

    while True:
        [exit() for event in pygame.event.get() if event.type == pygame.QUIT]


if __name__ == '__main__':
    main(MandelbrotConfig())
