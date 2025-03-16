import pygame
pygame.init()

from UI_elements.image_sequence import ImageSequence, ImageSeqConfig
from UI_elements.funny_text import HaloText, HaloTextConfig, ShadowedText, ShadowedTextConfig
from UI_elements.simple_buttons import SimpleButton, ButtonConfig
from UI_elements.input_field import InputFieldConfig, InputField

from constants.constants import *
from UI_scene.scene_class import Scene
from handlers.command_manager import CommandHandlerManager
from commands.trivial_commands import TestCommand
from commands.classificator_commands import CreateNewTag

import handlers.trivial_handlers as triv
import handlers.ui_interaction_handlers as ui_inter
import handlers.new_tag_handler as new_tag_handler


# noinspection PyPep8Naming
def create_test_UI_elements(images_folder) -> dict:
    return {
        'image_seq': ImageSequence(ImageSeqConfig(images_folder)),
        'input_field': InputField(InputFieldConfig('add new tag', 20, CreateNewTag())),
        'text1': ShadowedText(ShadowedTextConfig('Experimental Text')),
        'text2': HaloText(HaloTextConfig("Experimental Text")),
        'button1': SimpleButton(ButtonConfig("..АббРа__чистота..", TestCommand())),
        'button2': SimpleButton(ButtonConfig("virus research lab", TestCommand()))
    }


def scene_mainloop(screen: pygame.Surface, clock: pygame.time.Clock,
                   command_manager: CommandHandlerManager, scene: Scene):
    running = True
    while running:
        command_manager.handle_events()
        running = command_manager.is_running()

        screen.fill(SCREEN_FILLING_COLOR)

        scene.draw_elements(screen)
        pygame.display.flip()
        clock.tick(FPS)


def main(images_folder):
    screen = pygame.display.set_mode(WIN_SIZE)
    pygame.display.set_caption('Image Classifier')
    clock = pygame.time.Clock()

    scene = Scene('MainScene', create_test_UI_elements(images_folder))
    command_manager = CommandHandlerManager(scene)
    command_manager.register_many(
        [triv.TestCommandHandler(), ui_inter.SaveUIHandler(), triv.ExitHandler(), new_tag_handler.NewTagHandler()],
        [ui_inter.DraggingHandler(), ui_inter.HoverHandler(), ui_inter.CursorHandler()])

    scene_mainloop(screen, clock, command_manager, scene)

    pygame.quit()


if __name__ == '__main__':
    main('test_scripts/test_images')
