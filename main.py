import pygame
pygame.init()
import os
# import shutil
from UI_elements import simple_buttons, funny_text
from constants.constants import *
from UI_scene.scene import Scene
from handlers.command_manager import CommandHandlerManager
from commands.trivial_commands import TestCommand, TestCommand2
import handlers.trivial_handlers as triv
import handlers.dragging_handler as drag
import handlers.hover_handler as hover
import handlers.cursor_handler as cursor
from UI_elements.abstract_element import AbstractUIElement


def load_and_scale_image(image_path):
    image = pygame.image.load(image_path)
    orig_width, orig_height = image.get_size()

    scale_factor = min(MAX_IMAGE_WIDTH / orig_width, MAX_IMAGE_HEIGHT / orig_height)
    new_size = (int(orig_width * scale_factor), int(orig_height * scale_factor))

    return pygame.transform.smoothscale(image, new_size)


# noinspection PyPep8Naming
def create_test_UI_elements() -> list[AbstractUIElement]:
    add_tag_button_config = simple_buttons.ButtonConfig(
        text="virus research lab",
        command=TestCommand(),
        path_to_json='UI_elements/buttons_saves/add_tag_button.json'
    )
    test_button_1 = simple_buttons.SimpleButton(add_tag_button_config)

    add_tag_button_config = simple_buttons.ButtonConfig(
        text="..АббРа__чистота..",
        command=TestCommand2(),
        path_to_json='UI_elements/buttons_saves/test_2_button.json'
    )
    test_button_2 = simple_buttons.SimpleButton(add_tag_button_config)

    halo_text_config = funny_text.HaloTextConfig(
        text="Experimental Text",
        path_to_json='UI_elements/buttons_saves/text_element.json',
    )
    text_element = funny_text.HaloText(halo_text_config)

    # outline_text_config = funny_text.OutlinedTextConfig(
    #     text='Experimental Text',
    #     path_to_json='buttons_saves/text2_element.json',
    #     outline_color=(200, 50, 50),
    #     outline_extent=(1, 1)
    # )
    # text_element_2 = funny_text.OutlinedText(outline_text_config)
    shadow_text_config = funny_text.ShadowedTextConfig(
        path_to_json='UI_elements/buttons_saves/text2_element.json',
        text='Experimental Text',
        shadow_color=(255, 0, 0),
        shadow_offset=(1, 2),
    )
    text_element_2 = funny_text.ShadowedText(shadow_text_config)

    return [test_button_1, text_element, test_button_2, text_element_2]


def main(image_folder):
    screen = pygame.display.set_mode(WIN_SIZE)
    pygame.display.set_caption('Image Classifier')
    clock = pygame.time.Clock()

    all_elements = create_test_UI_elements()
    scene = Scene('Main', all_elements)

    images = [f for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
    if len(images) < 1:
        raise AssertionError('Zero images in image folder')
    image_index = 0
    image_name = images[image_index]
    image = load_and_scale_image(os.path.join(image_folder, image_name))

    command_manager = CommandHandlerManager(scene)
    command_manager.register(triv.TestCommandHandler())
    command_manager.register(triv.TestCommandHandler2())
    command_manager.register_family(drag.DraggingHandler())
    command_manager.register(triv.SaveUIHandler())
    command_manager.register_family(hover.HoverHandler())
    command_manager.register_family(cursor.CursorHandler())
    command_manager.register(triv.ExitHandler())

    running = True
    while running:
        command_manager.handle_events()

        screen.fill(SCREEN_FILLING_COLOR)
        if image_index < len(images):
            screen.blit(image, (0, 0))
        scene.draw_elements(screen)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == '__main__':
    # main('C:\\Users\\Игорь\\2')
    main('test_scripts/test_images')
