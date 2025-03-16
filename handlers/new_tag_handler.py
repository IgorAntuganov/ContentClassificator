from handlers.abstract_handlers import CommandHandler
from commands.classificator_commands import CreateNewTag


class NewTagHandler(CommandHandler):
    command_type = CreateNewTag

    def handler_func(self, command):
        print('Create New Tag')
