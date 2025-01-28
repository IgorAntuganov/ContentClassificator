from abc import ABC
from typing import TypeAlias
from dataclasses import dataclass

@dataclass
class CommandRequirements:
    element: bool = False
    scene: bool = False

class AbstractCommand(ABC):
    needs: CommandRequirements = CommandRequirements()

    def __init__(self):
        self._element = None
        self._scene = None

    @property
    def text(self):
        return self.__class__.__name__


    @property
    def need_element(self) -> bool:
        return self.needs.element

    @property
    def need_scene(self) -> bool:
        return self.needs.scene


    def set_element(self, element):
        self._element = element

    def get_element(self):
        return self._element

    def set_scene(self, scene):
        self._scene = scene

    def get_scene(self):
        return self._scene


class SimpleCommand(AbstractCommand, ABC):
    needs = CommandRequirements()

class ElementCommand(AbstractCommand, ABC):
    needs = CommandRequirements(element=True)

class SceneElementCommand(AbstractCommand, ABC):
    needs = CommandRequirements(element=True, scene=True)

class SceneCommand(AbstractCommand, ABC):
    needs = CommandRequirements(scene=True)


base_command_alias: TypeAlias = SimpleCommand | SceneElementCommand | ElementCommand | SceneCommand
CommandList = list[base_command_alias]
