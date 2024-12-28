import pygame
import os

def set_window_pos(x1, y1):
    os.environ['SDL_VIDEO_WINDOW_POS'] = f"{x1},{y1}"

def fill_screen(screen1):
    screen1.fill((30, 30, 30))
    font = pygame.font.Font(None, 36)
    text = font.render(f"Size: {width}x{height}", True, (200, 200, 200))
    screen1.blit(text, (10, 10))
    pygame.display.flip()


pygame.init()

# start sizes
width, height = 400, 300
# start position
x, y = 600, 600

set_window_pos(x, y)
screen = pygame.display.set_mode((width, height), pygame.NOFRAME)
fill_screen(screen)

running = True
clock = pygame.time.Clock()

while running:
    start_size = width, height
    start_pos = x, y

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_RIGHT:
                width += 10
            elif event.key == pygame.K_LEFT:
                width = max(200, width - 10)
            elif event.key == pygame.K_UP:
                height += 10
            elif event.key == pygame.K_DOWN:
                height = max(100, height - 10)
            elif event.key == pygame.K_w:
                y -= 50
            elif event.key == pygame.K_s:
                y += 50
            elif event.key == pygame.K_a:
                x -= 50
            elif event.key == pygame.K_d:
                x += 50

    if (x, y) != start_pos:
        pygame.display.quit()
    if (width, height) != start_size or (x, y) != start_pos:
        set_window_pos(x, y)
        screen = pygame.display.set_mode((width, height), pygame.NOFRAME)
        fill_screen(screen)

    clock.tick(60)

pygame.quit()
