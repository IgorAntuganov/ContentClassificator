import pygame
import os
import shutil
import sys
from commands import TextCommand as TexCom
import buttons
from constants import *
from states import MouseWheelState


def load_and_scale_image(image_path):
    image = pygame.image.load(image_path)
    orig_width, orig_height = image.get_size()

    scale_factor = min(MAX_IMAGE_WIDTH / orig_width, MAX_IMAGE_HEIGHT / orig_height)
    new_size = (int(orig_width * scale_factor), int(orig_height * scale_factor))

    return pygame.transform.smoothscale(image, new_size)


def main(image_folder, output_folder):
    pygame.init()

    screen = pygame.display.set_mode((WIN_SIZE))
    pygame.display.set_caption('Image Classifier')

    add_tag_button = buttons.Button("Добавить кнопку", TexCom('ADD_BUTTON'), (800, 50), (300, 60),
                                    BUTTON_COLOR_DICT2, fixed=False)
    tags_buttons = buttons.load_button_positions('tags_buttons.json')
    all_buttons = [add_tag_button] + tags_buttons

    images = [f for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
    image_index = 0
    image_name = images[image_index]
    image = load_and_scale_image(os.path.join(image_folder, image_name))

    all_done = False
    running = True
    while running:
        mouse_wheel_state = MouseWheelState.INACTIVE
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    mouse_wheel_state = MouseWheelState.UP
                elif event.button == 5:
                    mouse_wheel_state = MouseWheelState.DOWN
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                elif event.key == pygame.K_s:
                    if image_index < len(images)-1:
                        image_index += 1
                        image_name = images[image_index]
                        image = load_and_scale_image(os.path.join(image_folder, image_name))
                        all_done = True

        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        commands_pool = []
        for b in all_buttons:
            comm = b.handle_event(mouse_pos, mouse_pressed, mouse_wheel_state=mouse_wheel_state)
            if comm is not None:
                commands_pool.append(comm)

        screen.fill((0, 0, 0))
        if image_index < len(images):
            screen.blit(image, (0, 0))

        add_tag_button.draw(screen)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main('C:\\Users\\Игорь\\2', 'path/to/output_folder')
