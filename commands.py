from __future__ import annotations
from UI_element import UIElement
from abc import ABCMeta, abstractmethod, ABC


class BaseCommand:
    """Base command class"""
    def __init__(self, text: str):
        self.text = text

    def __hash__(self):
        return hash(self.__class__)

    def __eq__(self, other):
        return isinstance(other, self.__class__)


class UIElementCommand(BaseCommand):
    created_variants: set[str] = set()

    def __init__(self, element_association: UIElement):
        text = self.__class__.__name__
        super().__init__(self.__class__.__name__)
        self.created_variants.add(text)
        self._element_association: UIElement = element_association

    def get_element(self) -> UIElement:
        return self._element_association


# Commands initialization --------------------------------------------
ExitCommand = BaseCommand('Exit')


class FocusCommands(UIElementCommand, ABC): pass
class StartFocus(FocusCommands): pass
class KeepFocus(FocusCommands): pass
class EndFocus(FocusCommands): pass
