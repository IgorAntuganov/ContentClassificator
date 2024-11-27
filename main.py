import pygame
pygame.init()
import os
# import shutil
import sys
from commands import TextCommand as TexCom
import simple_buttons
import funny_text
from constants import *
from states import MouseWheelState
from UI_abstracts import EventConfig


def load_and_scale_image(image_path):
    image = pygame.image.load(image_path)
    orig_width, orig_height = image.get_size()

    scale_factor = min(MAX_IMAGE_WIDTH / orig_width, MAX_IMAGE_HEIGHT / orig_height)
    new_size = (int(orig_width * scale_factor), int(orig_height * scale_factor))

    return pygame.transform.smoothscale(image, new_size)


def get_ctrl_alt_shift_array() -> tuple[bool, bool, bool]:
    keys = pygame.key.get_pressed()
    ctrl_pressed = keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]
    alt_pressed = keys[pygame.K_LALT] or keys[pygame.K_RALT]
    shift_pressed = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
    return ctrl_pressed, alt_pressed, shift_pressed


def main(image_folder):
    pygame.init()

    screen = pygame.display.set_mode(WIN_SIZE)
    pygame.display.set_caption('Image Classifier')

    add_tag_button_config = simple_buttons.ButtonConfig(
        text="virus research lab",
        command=TexCom('ADD_BUTTON'),
        path_to_json='buttons_saves/add_tag_button.json'
    )
    add_tag_button = simple_buttons.SimpleButton(add_tag_button_config)

    halo_text_config = funny_text.HaloTextConfig(
        text="Experimental  Text",
        path_to_json='buttons_saves/text_element.json'
    )
    text_element = funny_text.HaloText(halo_text_config)

    # all_buttons = [add_tag_button]
    all_elements = [add_tag_button, text_element]

    images = [f for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
    image_index = 0
    image_name = images[image_index]
    image = load_and_scale_image(os.path.join(image_folder, image_name))

    # all_done = False
    running = True
    while running:
        ctrl_alt_shift_array = get_ctrl_alt_shift_array()
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
                        # all_done = True
                elif event.key == pygame.K_a:
                    for el in all_elements:
                        el.save_to_json()
                    print('elements saved')

        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        commands_pool = []
        event_config = EventConfig(mouse_position=mouse_pos,
                                   mouse_pressed=mouse_pressed,
                                   mouse_wheel_state=mouse_wheel_state,
                                   ctrl_alt_shift_array=ctrl_alt_shift_array)
        for el in all_elements:
            comm = el.handle_event(event_config)
            if comm is not None:
                commands_pool.append(comm)

        screen.fill((0, 0, 0))
        if image_index < len(images):
            screen.blit(image, (0, 0))

        for el in all_elements:
            el.draw(screen)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main('C:\\Users\\Игорь\\2')
