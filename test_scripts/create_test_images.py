import pygame
pygame.init()
import os
import random

directory = 'test_images'
formats: list[str] = ['png', 'jpg']
sizes: list[tuple[int, int]] = [
    (100, 100),
    (1920, 1080),
    (500, 800),
    (300, 400),
    (2560, 1080),
    (1280, 720),
    (720, 1280)
]

if not os.path.isdir(directory):
    os.mkdir(directory)

for width, height in sizes:
    image = pygame.Surface((width, height), pygame.SRCALPHA)

    color = [random.randint(50, 200) for _ in range(3)]
    for i in range(width//5+1):
        pygame.draw.rect(image, color, (i*15, 0, 5, height))
    for i in range(height//5+1):
        pygame.draw.rect(image, color, (0, i*15, width, 5))

    font_size = min(height, width) // 4
    font = pygame.font.Font(None, max(25, font_size))
    text = font.render('Test', 0, (255, 255, 250))
    text_rect = text.get_rect(center=image.get_rect().center)
    image.blit(text, text_rect)

    index = (width + height) % len(formats)
    _format = formats[index]
    file_name = f'{width}_{height}'
    file_path = f'{directory}/{file_name}.{_format}'
    pygame.image.save(image, file_path)
