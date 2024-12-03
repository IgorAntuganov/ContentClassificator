from abc import ABC, abstractmethod
from commands import BaseCommand, ExitCommand


class CommandHandlerManager:
    def __init__(self):
        self.handlers: dict[type: list[CommandHandler]] = {}

    def register(self, command_type, handler):
        if command_type not in self.handlers:
            self.handlers[command_type] = []
        self.handlers[command_type].append(handler)

    def handle_command(self, command: BaseCommand):
        handler = self.handlers.get(type(command))
        if handler:
            handler.handle(command)
        else:
            raise ValueError(f"No handler registered for command type {type(command)}")


class CommandHandler(ABC):
    def __init__(self, command_type: type, handler_func: callable):
        self.command_type = command_type
        self.handler_func = handler_func

    def handle(self, command: BaseCommand):
        if not isinstance(command, self.command_type):
            raise TypeError(f"Expected command of type {self.command_type}, got {type(command)}")
        self.handler_func(command)


def handle_exit():
    exit()


Exit_Handler = CommandHandler(BaseCommand, handle_exit)

CHM = CommandHandlerManager()
CHM.register(BaseCommand, Exit_Handler)
