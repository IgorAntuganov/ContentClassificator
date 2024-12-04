# from UI_element import UIElement
from dataclasses import dataclass, field, make_dataclass
from typing import ClassVar
import sys


class UIElement:
    pass


@dataclass
class CommandConfig:
    pass


@dataclass
class NoArgsConfig(CommandConfig):
    pass


@dataclass
class CustomConfig(CommandConfig):
    args: dict[str, type]


class CommandClassFabric:
    command_classes: ClassVar[dict[str, type]] = {}

    @classmethod
    def create(cls, name: str, config: CommandConfig) -> type:
        if isinstance(config, NoArgsConfig):
            fields = []
        elif isinstance(config, CustomConfig):
            fields = [(key, value, field()) for key, value in config.args.items()]
        else:
            raise ValueError("Invalid config type. Use NoArgsConfig or CustomConfig")

        command_class = make_dataclass(name, fields, bases=(CommandConfig,))
        cls.command_classes[name] = command_class

        return command_class

    @classmethod
    def verify_command_names(cls):
        current_module = sys.modules[__name__]
        for name, _class in cls.command_classes.items():
            if not hasattr(current_module, name) or getattr(current_module, name) is not _class:
                raise ValueError(f"Command class '{name}' is not correctly assigned to a variable with the same name" +
                                 '\nCorrect Example:' +
                                 '\nExitCommand = CommandClassFabric.create("ExitCommand", NO_ARGS)')
        print("\nAll command names verified successfully")


NO_ARGS = NoArgsConfig()
UI_ELEMENT = CustomConfig({'element': UIElement})
CREATE_NEW_PROFILE = CustomConfig({"name": str, "datetime": int, "language": str})

ExitCommand = CommandClassFabric.create("ExitCommand", NO_ARGS)
StartFocusCommand = CommandClassFabric.create("StartFocusCommand", UI_ELEMENT)

exit_command = ExitCommand()
print(type(exit_command))
print(exit_command)

button = UIElement()
start_focus_command = StartFocusCommand(element=button)
print(type(start_focus_command))
print(start_focus_command)


CreateNewProfileCommand = CommandClassFabric.create("CreateNewProfileCommand", CREATE_NEW_PROFILE)
profile_command = CreateNewProfileCommand("John", 1232131248712947, "en")
print(type(profile_command))
print(profile_command)
print(profile_command.fields)

# verifying command names, must be at the end of python file
CommandClassFabric.verify_command_names()
