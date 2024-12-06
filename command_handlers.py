from abc import abstractmethod, ABC
import commands
import UI_scene


class CommandHandler(ABC):
    @property
    @abstractmethod
    def command_type(self):
        pass

    def handle(self, command: commands.BaseCommand, scene: UI_scene.Scene):
        if not isinstance(command, self.command_type):
            raise TypeError(f"Expected command of type {self.command_type}, got {type(command)}")
        self.handler_func(command, scene)

    @abstractmethod
    def handler_func(self, command: commands.BaseCommand, scene: UI_scene.Scene):
        pass


class CommandFamilyHandler(CommandHandler, ABC):
    pass


# To do: auto register to manager
class ExitHandler(CommandHandler):  # Handlers classes ----------------
    command_type = commands.ExitCommand
    def handler_func(self, command: commands.ExitCommand, scene: UI_scene.Scene):
        print('Exit Command')
        exit()


class FocusHandler(CommandFamilyHandler):
    command_type = commands.FocusCommandFamily
    def handler_func(self, command: commands.FocusCommandFamily, scene: UI_scene.Scene):
        print('Focus?', command.text, command.get_element())


class TestCommandHandler(CommandHandler):
    command_type = commands.TestCommand
    def handler_func(self, command, scene):
        print('get TestCommand')
