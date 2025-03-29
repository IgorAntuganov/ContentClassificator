from UI_elements.image_sequence import ImageSequence, ImageSeqConfig
from UI_elements.funny_text import ShadowedText, ShadowedTextConfig
from UI_elements.simple_buttons import SimpleButton, ButtonConfig
from UI_elements.input_field import InputFieldConfig, InputField
from UI_scene.scene_class import Scene

from commands.trivial_commands import TestCommand
from commands.classificator_commands import CreateNewTag
from handlers.command_manager import UICommandHandlerManager, CommandHandlerManager

import handlers.trivial_handlers as triv
import handlers.new_tag_handler as new_tag_handler

from scene_creator import SceneCreator


class ImageTaggingSceneCreator(SceneCreator):
    def __init__(self, images_folder: str):
        elements = {
            'image_seq': ImageSequence(ImageSeqConfig(images_folder)),
            'input_field': InputField(InputFieldConfig('add new tag', 20, CreateNewTag())),
            'text1': ShadowedText(ShadowedTextConfig('Experimental Text')),
            'button1': SimpleButton(ButtonConfig("Button1", TestCommand())),
        }
        self.scene = Scene('ImageTagging', elements)
        self.command_manager = UICommandHandlerManager(self.scene)
        self.command_manager.register_many([triv.TestCommandHandler(),  new_tag_handler.NewTagHandler()], [])

    def get_scene_and_manager(self) -> tuple[Scene, CommandHandlerManager]:
        return self.scene, self.command_manager
