from UI_elements.abstract_element import UIElement
from UI_elements.input_field import InputField, InputFieldConfig
from UI_scene.scene_class import Scene
from handlers.command_manager import UICommandHandlerManager, CommandHandlerManager
from commands.add_folder_commands import AddFolderCommand

from scene_creator import SceneCreator


class AddFolderSceneCreator(SceneCreator):
    def __init__(self):
        pass

    def get_scene_and_manager(self) -> tuple[Scene, CommandHandlerManager]:
        elements: dict[str, UIElement] = {
            'FolderPathInput': InputField(InputFieldConfig('Enter path...', 200, AddFolderCommand())),
        }

        scene = Scene('AddFolder', elements)
        command_manager = UICommandHandlerManager(scene)
        handlers_lst = []
        family_lst = []
        command_manager.register_many(handlers_lst, family_lst)
        return scene, command_manager
