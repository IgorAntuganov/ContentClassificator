from abc import ABC
import command_handlers as ch
import commands


class CommandHandlerManager:
    def __init__(self):
        self.handlers: dict[type: list[ch.CommandHandler]] = {}
        self.family_handlers: dict[type: list[ch.CommandHandler]] = {}

    def register(self, handler: ch.CommandHandler):
        com_type = handler.command_type
        print('registering', com_type)

        if com_type not in self.handlers:
            self.handlers[com_type] = []
        self.handlers[com_type].append(handler)

    def register_family(self, family_handler: ch.CommandFamilyHandler):
        com_family_type = family_handler.command_type
        if not issubclass(com_family_type, ABC):
            raise TypeError(f"Family handler must be ABC subclass. "
                            f"Wrong handler: {com_family_type}")
        if not issubclass(com_family_type, commands.CommandFamily):
            raise TypeError(f"Family handler must be CommandFamilyHandler subclass. "
                            f"Wrong handler: {com_family_type}")
        print('registering family', com_family_type)

        for child_class in com_family_type.__subclasses__():
            print('registering', child_class)
            if child_class not in self.handlers:
                self.handlers[child_class] = []
            self.handlers[child_class].append(family_handler)

    def handle_command(self, command):
        handlers = self.handlers.get(type(command))
        if not handlers:
            raise ValueError(f"No handler registered for command type {type(command)}"
                             f"\nRegistered commands: {list(self.handlers.keys())}")
        for handler in handlers:
            handler.handle(command)

    def handle_commands(self, commands_pool):
        for command in commands_pool:
            self.handle_command(command)


CHM = CommandHandlerManager()
CHM.register(ch.ExitHandler())
CHM.register(ch.TestCommandHandler())
CHM.register_family(ch.FocusHandler())
