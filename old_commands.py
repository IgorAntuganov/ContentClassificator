from __future__ import annotations
from UI_element import UIElement


class BaseCommand:
    """Base command class"""
    def __init__(self, text: str):
        self.text = text

    def __eq__(self, other):
        return self.text == other.text


ExitCommand = BaseCommand('EXIT')


class CommandWithElement(BaseCommand):
    def __init__(self, text: str):
        super().__init__(text)
        self.element_association: None | UIElement = None

    def set_element_association(self, el: UIElement) -> CommandWithElement:
        self.element_association = el
        return self

    def clear_element_association(self):
        self.element_association = None

    def is_element_set(self) -> bool:
        return self.element_association is not None

    def get_element(self) -> UIElement:
        assert self.element_association is not None
        return self.element_association


StartFocus = CommandWithElement('START_FOCUS')
KeepFocus = CommandWithElement('KEEP_FOCUS')
EndFocus = CommandWithElement('END_FOCUS')
