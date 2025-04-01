from UI_elements.input_field import InputField
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
        print('extracred: ', extracted_path)
        self.source_folders.append(extracted_path)
