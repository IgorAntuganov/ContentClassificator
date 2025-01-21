from abc import abstractmethod, ABC
from commands.abstract_commands import BaseCommand


class CommandHandler(ABC):
    @property
    @abstractmethod
    def command_type(self):
        pass

    def handle(self, command: BaseCommand):
        if not isinstance(command, self.command_type):
            raise TypeError(f"Expected command of type {self.command_type}, got {type(command)}")
        self.handler_func(command)

    @abstractmethod
    def handler_func(self, command: BaseCommand):
        pass


class CommandFamilyHandler(CommandHandler, ABC):
    pass
