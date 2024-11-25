import random
import pygame
pygame.init()
import time
# import string

font = pygame.font.Font('fonts_variants/test_font.ttf', 28)

image = pygame.Surface((1920, 2160))
image.fill((240, 240, 240))

for i in range(50):
    # symbols = string.ascii_lowercase * 2 + string.ascii_uppercase
    # symbols_list = list(symbols)
    # random.shuffle(symbols_list)
    # text = ''.join(symbols_list)
    text = ''.join([chr(random.randint(48, 122)) for _ in range(80)])
    text_surface = font.render(text, 1, (30, 30, 30))
    image.blit(text_surface, (50, i * 40 + 50))

time_mark = int(time.time() * 100)
pygame.image.save(image, f'fonts_variants/{time_mark}.png')
