from __future__ import annotations
from UI_elements.abstract_element import AbstractUIElement
from abc import ABC, abstractmethod


class BaseCommand(ABC):
    """Base command class"""
    @property
    @abstractmethod
    def text(self):
        pass

    def __init__(self):
        pass

    def __hash__(self):
        return hash(self.text)

    def __eq__(self, other):
        return isinstance(other, self.__class__)


class UIElementCommand(BaseCommand):
    @property
    def text(self):
        return self.__class__.__name__

    def __init__(self, element_association: AbstractUIElement):
        super().__init__()
        self._element_association: AbstractUIElement = element_association

    def get_element(self) -> AbstractUIElement:
        return self._element_association


class CommandFamily:
    """Base command family class"""
    pass
