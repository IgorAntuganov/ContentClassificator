from UI_elements.folder_icon import FolderIcon, generate_element_name
from UI_elements.input_field import InputField
from UI_scene.scene_class import Scene
from commands.abstract_commands import AbstractCommand
from json_storage import JsonListStorage
from handlers.abstract_handlers import CommandHandler
from commands.classificator_commands import AddSourceFolder


class NewSourceFolderHandler(CommandHandler):
    command_type = AddSourceFolder

    def __init__(self, source_folders: JsonListStorage):
        self.source_folders = source_folders

    def handler_func(self, command: AbstractCommand):
        element: InputField = command.get_element()
        extracted_path = element.extract_text()
        self.source_folders.append(extracted_path)

        new_folder_icon = FolderIcon(extracted_path)
        new_element_name = generate_element_name(extracted_path)
        scene: Scene = command.get_scene()
        scene.add_new_element(new_element_name, new_folder_icon)
