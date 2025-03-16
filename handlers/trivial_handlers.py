from handlers.abstract_handlers import CommandHandler
from commands.trivial_commands import ExitCommand, TestCommand


class ExitHandler(CommandHandler):
    command_type = ExitCommand

    def handler_func(self, command):
        print('Exit Command')
        exit()


class TestCommandHandler(CommandHandler):
    command_type = TestCommand

    def handler_func(self, command):
        print('get TestCommand')
