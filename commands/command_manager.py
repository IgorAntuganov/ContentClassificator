from abc import ABC
from constants import debug_print_1
from commands.scene_manager_protocols import SceneProtocol, CommandHandlerProtocol, CommandHandlerFamilyProtocol
from commands.abstract_commands import CommandFamily, BaseCommand


class CommandHandlerManager:
    def __init__(self, scene: SceneProtocol | None = None):
        self.scene: SceneProtocol | None = scene
        self.handlers: dict[type, list[CommandHandlerProtocol]] = {}
        self.family_handlers: dict[type, list[CommandHandlerProtocol]] = {}

    def set_scene(self, scene: SceneProtocol):
        self.scene = scene

    def register(self, handler: CommandHandlerProtocol):
        com_type = handler.command_type
        debug_print_1('registering', com_type)

        if com_type not in self.handlers:
            self.handlers[com_type] = []
        self.handlers[com_type].append(handler)

    def register_family(self, family_handler: CommandHandlerFamilyProtocol):
        com_family_type = family_handler.command_type
        if not issubclass(com_family_type, ABC):
            raise TypeError(f"Family handler must be ABC subclass. "
                            f"Wrong handler: {com_family_type}")
        if not issubclass(com_family_type, CommandFamily):
            raise TypeError(f"Family handler must be CommandFamilyHandler subclass. "
                            f"Wrong handler: {com_family_type}")
        debug_print_1('registering family', com_family_type)

        for child_class in com_family_type.__subclasses__():
            debug_print_1('registering family member', child_class)
            if child_class not in self.handlers:
                self.handlers[child_class] = []
            self.handlers[child_class].append(family_handler)

    def handle_command(self, command):
        assert self.scene is not None
        if self.scene is None:
            raise AssertionError('CommandHandlerManager scene is not defined. Use set_scene()')
        handlers = self.handlers.get(type(command))
        if not handlers:
            raise ValueError(f"No handler registered for command type {type(command)}"
                             f"\nRegistered commands: {list(self.handlers.keys())}")
        for handler in handlers:
            handler.handle(command, self.scene)

    def handle_commands(self, commands_pool):
        if self.scene is None:
            raise AssertionError('CommandHandlerManager scene is not defined. Use set_scene()')
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
