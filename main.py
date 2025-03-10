import pygame


pygame.init()
# import shutil

from UI_elements.image_sequence import ImageSequence, ImageSeqConfig
from UI_elements.funny_text import HaloText, HaloTextConfig, ShadowedText, ShadowedTextConfig
from UI_elements.simple_buttons import SimpleButton, ButtonConfig
from UI_elements.input_field import InputFieldConfig, InputField

from constants.constants import *
from UI_scene.scene_class import Scene
from handlers.command_manager import CommandHandlerManager
from commands.trivial_commands import TestCommand, TestCommand2

import handlers.trivial_handlers as triv
import handlers.ui_saving_handler as ui_save
import handlers.dragging_handler as drag
import handlers.hover_handler as hover
import handlers.cursor_handler as cursor


# noinspection PyPep8Naming
def create_test_UI_elements(images_folder) -> dict:
    return {
        'image_seq': ImageSequence(ImageSeqConfig(images_folder)),
        'input_field': InputField(InputFieldConfig('input...', 20)),
        'text1': ShadowedText(ShadowedTextConfig('Experimental Text')),
        'text2': HaloText(HaloTextConfig("Experimental Text")),
        'button1': SimpleButton(ButtonConfig("..АббРа__чистота..", TestCommand2())),
        'button2': SimpleButton(ButtonConfig("virus research lab", TestCommand()))
    }


def main(images_folder):
    screen = pygame.display.set_mode(WIN_SIZE)
    pygame.display.set_caption('Image Classifier')
    clock = pygame.time.Clock()

    scene = Scene('MainScene', create_test_UI_elements(images_folder))

    command_manager = CommandHandlerManager(scene)
    command_manager.register(triv.TestCommandHandler())
    command_manager.register(triv.TestCommandHandler2())
    command_manager.register_family(drag.DraggingHandler())
    command_manager.register(ui_save.SaveUIHandler())
    command_manager.register_family(hover.HoverHandler())
    command_manager.register_family(cursor.CursorHandler())
    command_manager.register(triv.ExitHandler())

    running = True
    while running:
        command_manager.handle_events()

        screen.fill(SCREEN_FILLING_COLOR)

        scene.draw_elements(screen)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == '__main__':
    main('test_scripts/test_images')
