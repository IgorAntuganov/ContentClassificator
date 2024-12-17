import random
import pygame
pygame.init()
import time

font = pygame.font.Font('test_font.ttf', 30)

image = pygame.Surface((1920, 2160))
image.fill((240, 240, 240))

for i in range(50):
    text = ''.join([chr(random.randint(48, 122)) for _ in range(80)])
    text_surface = font.render(text, 1, (30, 30, 30))
    image.blit(text_surface, (50, i * 40 + 50))

time_mark = int(time.time() * 100)
pygame.image.save(image, f'font_renders/{time_mark}.png')
