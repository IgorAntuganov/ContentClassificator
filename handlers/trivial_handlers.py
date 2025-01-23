from UI_elements import UI_abstracts
from handlers.abstract_handlers import CommandHandler
from commands.trivial_commands import ExitCommand, TestCommand, TestCommand2, SaveUICommand
from UI_scene.scene import Scene


class ExitHandler(CommandHandler):
    command_type = ExitCommand
    def handler_func(self, command):
        print('Exit Command')
        exit()

class TestCommandHandler(CommandHandler):
    command_type = TestCommand
    def handler_func(self, command):
        print('get TestCommand')

class TestCommandHandler2(CommandHandler):
    command_type = TestCommand2
    def handler_func(self, command):
        print('get TestCommand (2!!)')

class SaveUIHandler(CommandHandler):
    command_type = SaveUICommand
    def handler_func(self, command):
        command: SaveUICommand
        scene = command.get_scene()
        scene: Scene
        element_manager = scene.get_elements_manager()
        for el in element_manager.get_ordered_elements():
            assert isinstance(el, UI_abstracts.JSONadjustable)
            el.save_to_json()
        print('UI saved')
