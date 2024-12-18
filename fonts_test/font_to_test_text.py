import random
import pygame
pygame.init()
import time

font = pygame.font.Font('kerned_AtoP.ttf', 50)

image = pygame.Surface((3840, 2160))
image.fill((240, 240, 240))

for i in range(35):
    print(f'\r{i+1} of 35', end='')
    text = ''.join([chr(random.randint(48, 122)) for _ in range(115)])
    text_surface = font.render(text, 1, (30, 30, 30))
    image.blit(text_surface, (50, i * 60 + 50))
print()

time_mark = int(time.time() * 100)
pygame.image.save(image, f'font_renders/{time_mark}.png')
