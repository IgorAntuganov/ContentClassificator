import pygame
pygame.init()
import os
# import shutil
import sys
import commands
import simple_buttons
import funny_text
from constants import *
import UI_scene
from command_manager import CHM


def load_and_scale_image(image_path):
    image = pygame.image.load(image_path)
    orig_width, orig_height = image.get_size()

    scale_factor = min(MAX_IMAGE_WIDTH / orig_width, MAX_IMAGE_HEIGHT / orig_height)
    new_size = (int(orig_width * scale_factor), int(orig_height * scale_factor))

    return pygame.transform.smoothscale(image, new_size)


def main(image_folder):
    screen = pygame.display.set_mode(WIN_SIZE)
    pygame.display.set_caption('Image Classifier')
    clock = pygame.time.Clock()

    add_tag_button_config = simple_buttons.ButtonConfig(
        text="virus research lab",
        command=commands.TestCommand(),
        path_to_json='buttons_saves/add_tag_button.json'
    )
    test_button_1 = simple_buttons.SimpleButton(add_tag_button_config)

    add_tag_button_config = simple_buttons.ButtonConfig(
        text="..AbraCadabra..",
        command=commands.TestCommand2(),
        path_to_json='buttons_saves/test_2_button.json'
    )
    test_button_2 = simple_buttons.SimpleButton(add_tag_button_config)

    halo_text_config = funny_text.HaloTextConfig(
        text="Experimental  Text",
        path_to_json='buttons_saves/text_element.json'
    )
    text_element = funny_text.HaloText(halo_text_config)

    all_elements = [test_button_1, text_element, test_button_2]

    images = [f for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
    image_index = 0
    image_name = images[image_index]
    image = load_and_scale_image(os.path.join(image_folder, image_name))

    scene = UI_scene.Scene('Main', all_elements, 1)
    CHM.set_scene(scene)

    running = True
    while running:
        commands_pool = scene.handle_events()
        CHM.handle_commands(commands_pool)

        # unhandled_commands = []
        # for command in commands_pool:
        #     if BaseCommand('NEXT_IMAGE') == command:
        #         if image_index < len(images)-1:
        #             image_index += 1
        #             image_name = images[image_index]
        #             image = load_and_scale_image(os.path.join(image_folder, image_name))
        #     elif BaseCommand('SAVE_UI') == command:
        #         for el in all_elements:
        #             el.save_to_json()
        #         print('UI Saved')
        #     elif ExitCommand == command:
        #         running = False
        #     elif type(command) == BaseCommand:
        #         command: BaseCommand
        #         print('text command', command.text)
        #     else:
        #         unhandled_commands.append(command)
        # assert len(unhandled_commands) == 0

        screen.fill(SCREEN_FILLING_COLOR)
        if image_index < len(images):
            screen.blit(image, (0, 0))
        scene.draw_elements(screen)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main('C:\\Users\\Игорь\\2')
