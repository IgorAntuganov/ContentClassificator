from commands.abstract_handlers import CommandHandler
from commands.abstract_commands import BaseCommand


class ExitCommand(BaseCommand):
    text = 'Exit'
class TestCommand(BaseCommand):
    text = 'Test'
class TestCommand2(BaseCommand):
    text = 'Test_2'
class SaveUICommand(BaseCommand):
    text = 'Save_UI'


class ExitHandler(CommandHandler):
    command_type = ExitCommand
    def handler_func(self, command, scene):
        print('Exit Command')
        exit()

class TestCommandHandler(CommandHandler):
    command_type = TestCommand
    def handler_func(self, command, scene):
        print('get TestCommand')

class TestCommandHandler2(CommandHandler):
    command_type = TestCommand2
    def handler_func(self, command, scene):
        print('get TestCommand (2!!)')

class SaveUIHandler(CommandHandler):
    command_type = SaveUICommand
    def handler_func(self, command, scene):
        scene.save_elements()
        print('UI saved')