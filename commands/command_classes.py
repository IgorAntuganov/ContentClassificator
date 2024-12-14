from __future__ import annotations
from UI_element import MetaUIElement
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

    def __init__(self, element_association: MetaUIElement):
        super().__init__()
        self._element_association: MetaUIElement = element_association

    def get_element(self) -> MetaUIElement:
        return self._element_association


class CommandFamily:
    pass


# Commands initialization --------------------------------------------
class ExitCommand(BaseCommand):
    text = 'Exit'
class TestCommand(BaseCommand):
    text = 'Test'
class TestCommand2(BaseCommand):
    text = 'Test_2'
class SaveUICommand(BaseCommand):
    text = 'Save_UI'


class DraggingCommandFamily(CommandFamily, UIElementCommand, ABC): pass
class StartDragging(DraggingCommandFamily): pass
class KeepDragging(DraggingCommandFamily): pass
class EndDragging(DraggingCommandFamily): pass


class HoverCommandFamily(CommandFamily, UIElementCommand, ABC): pass
class StartHover(HoverCommandFamily): pass
class KeepHover(HoverCommandFamily): pass
class EndHover(HoverCommandFamily): pass
