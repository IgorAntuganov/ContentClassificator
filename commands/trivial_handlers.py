from commands.command_handlers import CommandHandler
import commands.command_classes as com_classes


class ExitHandler(CommandHandler):
    command_type = com_classes.ExitCommand
    def handler_func(self, command, scene):
        print('Exit Command')
        exit()

class TestCommandHandler(CommandHandler):
    command_type = com_classes.TestCommand
    def handler_func(self, command, scene):
        print('get TestCommand')

class TestCommandHandler2(CommandHandler):
    command_type = com_classes.TestCommand2
    def handler_func(self, command, scene):
        print('get TestCommand (2!!)')

class SaveUIHandler(CommandHandler):
    command_type = com_classes.SaveUICommand
    def handler_func(self, command, scene):
        scene.save_elements()
        print('UI saved')
