from abc import abstractmethod, ABC
import commands


class CommandHandler(ABC):
    @property
    @abstractmethod
    def command_type(self):
        pass

    def handle(self, command):
        if not isinstance(command, self.command_type):
            raise TypeError(f"Expected command of type {self.command_type}, got {type(command)}")
        self.handler_func(command)

    @abstractmethod
    def handler_func(self, command):
        pass


class CommandFamilyHandler(CommandHandler, ABC):
    pass


# To do: auto register to manager
class ExitHandler(CommandHandler):  # Handlers classes ----------------
    command_type = commands.ExitCommand
    def handler_func(self, command: commands.ExitCommand):
        exit()


class FocusHandler(CommandFamilyHandler):
    command_type = commands.FocusCommandFamily
    def handler_func(self, command: commands.FocusCommandFamily):
        print('Focus?', command.text, command.get_element())


class TestCommandHandler(CommandHandler):
    command_type = commands.TestCommand
    def handler_func(self, command):
        print('get TestCommand')
