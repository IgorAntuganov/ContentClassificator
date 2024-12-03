# from UI_element import UIElement
from dataclasses import dataclass, field, make_dataclass
from typing import Type, Any, Dict


class UIElement:
    pass


@dataclass
class CommandConfig:
    pass


@dataclass
class NoArgsConfig(CommandConfig):
    pass


@dataclass
class UIElementConfig(CommandConfig):
    element_type: Type[Any]


@dataclass
class CustomConfig(CommandConfig):
    args: Dict[str, Type[Any]]


class CommandClassFabric:
    command_classes: Dict[str, Type] = {}

    @classmethod
    def create(cls, name: str, config: CommandConfig) -> Type:
        fields = []

        if isinstance(config, NoArgsConfig):
            pass
        elif isinstance(config, UIElementConfig):
            fields.append(('element', config.element_type, field()))
        elif isinstance(config, CustomConfig):
            fields.extend((key, value, field()) for key, value in config.args.items())
        else:
            raise ValueError("Invalid config type")

        command_class = make_dataclass(name, fields, bases=(CommandConfig,))
        cls.command_classes[name] = command_class

        return command_class

    @classmethod
    def verify_command_names(cls):
        import sys
        current_module = sys.modules[__name__]
        for name, _class in cls.command_classes.items():
            if not hasattr(current_module, name) or getattr(current_module, name) is not _class:
                raise ValueError(f"Command class '{name}' is not correctly assigned to a variable with the same name" +
                                 '\nCorrect Example:' +
                                 '\nExitCommand = CommandClassFabric.create("ExitCommand", NO_ARGS)')
        print("\nAll command names verified successfully")


NO_ARGS = NoArgsConfig()
UI_ELEMENT = UIElementConfig(UIElement)


ExitCommand = CommandClassFabric.create("ExitComman", NO_ARGS)
SaveUICommand = CommandClassFabric.create("SaveUICommand", NO_ARGS)
StartFocusCommand = CommandClassFabric.create("StartFocusCommand", UI_ELEMENT)
EndFocusCommand = CommandClassFabric.create("EndFocusCommand", UI_ELEMENT)


from datetime import datetime
CreateNewProfileCommand = CommandClassFabric.create("CreateNewProfileCommand",
                                                    CustomConfig({"name": str, "date": datetime, "language": str}))


exit_command = ExitCommand()
print(type(exit_command))
print(exit_command)

button = UIElement()
start_focus_command = StartFocusCommand(element=button)
print(type(start_focus_command))
print(start_focus_command)


# verifying command names
CommandClassFabric.verify_command_names()
