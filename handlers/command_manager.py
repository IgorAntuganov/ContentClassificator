from abc import ABC
from constants.debug_prints import debug_print, DebugStates
from handlers.abstract_handlers import CommandHandler
from commands.abstract_commands import SceneElementCommand, ElementCommand, base_command_alias
from UI_scene.scene_class import Scene
from UI_elements.abstract_element import UIElement


class CommandHandlerManager:
    def __init__(self, scene: Scene):
        self.handlers: dict[type, CommandHandler] = {}
        self.family_handlers: dict[type, CommandHandler] = {}
        self._scene = scene

    def register(self, handler: CommandHandler):
        self._validate_registration(handler)
        com_type = handler.command_type
        debug_print(DebugStates.HANDLERS_REGISTERING, 'registering', com_type)
        self.handlers[com_type] = handler

    def register_family(self, family_handler: CommandHandler):
        self._verify_family_registration(family_handler)
        com_family_type = family_handler.command_type
        debug_print(DebugStates.HANDLERS_REGISTERING, 'registering family', com_family_type)

        for child_class in com_family_type.__subclasses__():
            debug_print(DebugStates.HANDLERS_REGISTERING, '\tregistering family member', child_class)
            self.handlers[child_class] = family_handler

    def handle_events(self):
        for commands_lst in self._scene.handle_events():
            for command in commands_lst:
                self._handle_command(command)

    def _handle_command(self, command):
        self._verify_command(command)
        handler = self.handlers[type(command)]
        handler.handle(command)

    # Checking for errors methods
    @staticmethod
    def _validate_registration(handler: CommandHandler):
        com_type = handler.command_type
        if not issubclass(com_type, base_command_alias):
            raise TypeError(f"Handler command type must be one of base command classes.\n"
                            f"Wrong handler: {com_type}\n"
                            f"Possible command types: {base_command_alias}")

    @staticmethod
    def _verify_family_registration(family_handler: CommandHandler):
        com_family_type = family_handler.command_type
        if not issubclass(com_family_type, ABC):
            raise TypeError(f"Family handler must be ABC subclass. "
                            f"Wrong handler: {com_family_type}")
        if not issubclass(com_family_type, base_command_alias):
            raise TypeError(f"Family handler command type must be CommandFamily subclass. "
                            f"Wrong handler: {com_family_type}")

    def _verify_command(self, command):
        if isinstance(command, SceneElementCommand) and command.get_scene() is None:
            raise ValueError(f"SceneCommand scene attribute is not defined. Command: {command}")
        if isinstance(command, SceneElementCommand) and command.get_element() is None:
            raise ValueError(f"SceneCommand element attribute is not defined. Command: {command}")

        if isinstance(command, ElementCommand) and command.get_element() is None:
            raise ValueError(f"ElementCommand element attribute is not defined. Command: {command}")

        if command.get_scene() is not None and not isinstance(command.get_scene(), Scene):
            raise TypeError(f"Scene attribute of command is not Scene type. Command: {command}")
        if command.get_element() is not None and not isinstance(command.get_element(), UIElement):
            raise TypeError(f"Element attribute of command is not one of base command types. Command: {command}")

        handlers = self.handlers.get(type(command))
        if not handlers:
            raise ValueError(f"No handler registered for command type {type(command)}"
                             f"\nRegistered commands: {list(self.handlers.keys())}")
