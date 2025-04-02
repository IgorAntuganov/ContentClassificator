from UI_elements.abstract_element import UIElement
from UI_elements.input_field import InputField, InputFieldConfig
from UI_elements.folder_icon import FolderIcon, generate_element_name
from UI_scene.scene_class import Scene
from handlers.command_manager import UICommandHandlerManager, CommandHandlerManager
from handlers.source_folders_handler import NewSourceFolderHandler
from commands.classificator_commands import AddSourceFolder

from scene_creator import SceneCreator
from json_storage import JsonListStorage
FOLDERS_SAVE_PATH = 'Data/source_folders.json'


class AddFolderSceneCreator(SceneCreator):
    def __init__(self):
        self.source_folders = JsonListStorage(FOLDERS_SAVE_PATH)

    def get_scene_and_manager(self) -> tuple[Scene, CommandHandlerManager]:
        folders_elements = {}
        for i, folder_path in enumerate(self.source_folders):
            folders_elements[generate_element_name(folder_path)] = FolderIcon(folder_path)

        elements: dict[str, UIElement] = {
            'FolderPathInput': InputField(InputFieldConfig('Enter path...', 80, AddSourceFolder())),
        }
        elements.update(folders_elements)

        scene = Scene('AddFolder', elements)
        command_manager = UICommandHandlerManager(scene)
        handlers_lst = [NewSourceFolderHandler(self.source_folders)]
        family_lst = []
        command_manager.register_many(handlers_lst, family_lst)
        return scene, command_manager
