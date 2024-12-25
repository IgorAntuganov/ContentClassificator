import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))

system_cursors = {
    'arrow': pygame.SYSTEM_CURSOR_ARROW,
    'ibeam': pygame.SYSTEM_CURSOR_IBEAM,
    'wait': pygame.SYSTEM_CURSOR_WAIT,
    'crosshair': pygame.SYSTEM_CURSOR_CROSSHAIR,
    'waitarrow': pygame.SYSTEM_CURSOR_WAITARROW,
    'sizenwse': pygame.SYSTEM_CURSOR_SIZENWSE,
    'sizenesw': pygame.SYSTEM_CURSOR_SIZENESW,
    'sizewe': pygame.SYSTEM_CURSOR_SIZEWE,
    'sizens': pygame.SYSTEM_CURSOR_SIZENS,
    'sizeall': pygame.SYSTEM_CURSOR_SIZEALL,
    'no': pygame.SYSTEM_CURSOR_NO,
    'hand': pygame.SYSTEM_CURSOR_HAND,
}

current_cursor = 'arrow'

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                cursors = list(system_cursors.keys())
                current_index = cursors.index(current_cursor)
                next_index = (current_index + 1) % len(cursors)
                current_cursor = cursors[next_index]
                pygame.mouse.set_cursor(system_cursors[current_cursor])
pygame.quit()
