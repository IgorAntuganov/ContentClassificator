from abc import ABC, abstractmethod


class Command:
    @abstractmethod
    def to_json(self) -> str:
        pass


class TextCommand(Command):
    def __init__(self, text):
        self.text = text

    def to_json(self) -> str:
        return self.text

    def __eq__(self, other):
        return self.text == other.text


class ExitCommand(TextCommand):
    def __init__(self):
        super().__init__('EXIT')
