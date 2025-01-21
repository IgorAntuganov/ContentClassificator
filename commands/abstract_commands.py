from __future__ import annotations
from UI_elements.abstract_element import AbstractUIElement
from abc import ABC, abstractmethod

from commands.scene_manager_protocols import SceneProtocol


class BaseCommand(ABC):
    """Base command class"""
    @property
    @abstractmethod
    def text(self):
        pass


class SceneCommand(BaseCommand, ABC):
    @property
    def text(self):
        return self.__class__.__name__

    def __init__(self):
        super().__init__()
        self._scene_association: None | SceneProtocol = None

    def set_scene(self, scene: SceneProtocol):
        self._scene_association = scene

    def get_scene(self) -> SceneProtocol:
        return self._scene_association


class UIElementCommand(SceneCommand, ABC):
    def __init__(self, element_association: AbstractUIElement):
        super().__init__()
        self._element_association: AbstractUIElement = element_association

    def get_element(self) -> AbstractUIElement:
        return self._element_association


class CommandFamily:
    """Base command family class"""
    pass
