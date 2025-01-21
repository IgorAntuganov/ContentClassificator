from abc import ABC
from constants.debug_prints import debug_print, DebugStates
from commands.abstract_handlers import CommandHandler, CommandFamilyHandler
from commands.abstract_commands import CommandFamily, BaseCommand, SceneCommand


class CommandHandlerManager:
    def __init__(self):
        self.handlers: dict[type, CommandHandler] = {}
        self.family_handlers: dict[type, CommandHandler] = {}

    def register(self, handler: CommandHandler):
        self._validate_registration(handler)
        com_type = handler.command_type
        debug_print(DebugStates.HANDLERS_REGISTERING, 'registering', com_type)
        self.handlers[com_type] = handler

    def register_family(self, family_handler: CommandFamilyHandler):
        self._verify_family_registration(family_handler)
        com_family_type = family_handler.command_type
        debug_print(DebugStates.HANDLERS_REGISTERING, 'registering family', com_family_type)

        for child_class in com_family_type.__subclasses__():
            debug_print(DebugStates.HANDLERS_REGISTERING, '\tregistering family member', child_class)
            self.handlers[child_class] = family_handler


    def handle_command(self, command):
        self._verify_command(command)
        handler = self.handlers.get(type(command))
        handler.handle(command)

    def handle_commands(self, commands_pool):
        for command in commands_pool:
            self.handle_command(command)


    def filter_handleable(self, commands_lst: list[BaseCommand]) -> list[BaseCommand]:
        filtered = []
        for comm in commands_lst:
            if type(comm) in self.handlers:
                filtered.append(comm)
        return filtered

    def filter_non_handleable(self, commands_lst: list[BaseCommand]) -> list[BaseCommand]:
        filtered = []
        for comm in commands_lst:
            if type(comm) not in self.handlers:
                filtered.append(comm)
        return filtered


    # Checking for errors methods
    @staticmethod
    def _validate_registration(handler: CommandHandler):
        com_type = handler.command_type
        if not issubclass(com_type, BaseCommand):
            raise TypeError(f"Handler command type must be BaseCommand subclass. "
                            f"Wrong handler: {com_type}")
        if issubclass(com_type, CommandFamily):
            raise TypeError(f"Handler command type mustn't be CommandFamily subclass. "
                            f"Wrong handler: {com_type}")

    @staticmethod
    def _verify_family_registration(family_handler: CommandFamilyHandler):
        com_family_type = family_handler.command_type
        if not issubclass(com_family_type, ABC):
            raise TypeError(f"Family handler must be ABC subclass. "
                            f"Wrong handler: {com_family_type}")
        if not issubclass(com_family_type, CommandFamily):
            raise TypeError(f"Family handler command type must be CommandFamily subclass. "
                            f"Wrong handler: {com_family_type}")

    def _verify_command(self, command):
        if isinstance(command, SceneCommand) and command.get_scene() is None:
            raise ValueError(f"SceneCommand scene attribute is not defined. Command: {command}")
        handlers = self.handlers.get(type(command))
        if not handlers:
            raise ValueError(f"No handler registered for command type {type(command)}"
                             f"\nRegistered commands: {list(self.handlers.keys())}")
