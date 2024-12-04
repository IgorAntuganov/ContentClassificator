from abc import abstractmethod, ABCMeta, ABC
from commands import BaseCommand, ExitCommand, UIElementCommand, FocusCommands, StartFocus


class CommandHandler(metaclass=ABCMeta):
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


class ExitHandler(CommandHandler):  # Handlers classes ----------------
    command_type = ExitCommand
    def handler_func(self, command: ExitCommand):
        exit()


class FocusHandler(CommandHandler):
    command_type = FocusCommands
    def handler_func(self, command: FocusCommands):
        print('Focus?', command.text, command.get_element())


class CommandHandlerManager:  # Manager class -----------------------
    def __init__(self):
        self.handlers: dict[type: list[CommandHandler]] = {}

    def register(self, handler: CommandHandler):
        com_type = handler.command_type
        print('registing', com_type, f'({handler.command_type})')
        print(type(handler), type(handler.command_type))
        if com_type not in self.handlers:
            self.handlers[com_type] = []
        self.handlers[com_type].append(handler)

    def handle_command(self, command):
        handler = self.handlers.get(type(command))
        if handler:
            handler.handle(command)
        else:
            raise ValueError(f"No handler registered for command type {type(command)}"
                             f"\nRegistered commands: {list(self.handlers.keys())}")


CHM = CommandHandlerManager()
CHM.register(ExitHandler())
CHM.register(FocusHandler())
