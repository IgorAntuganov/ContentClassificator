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
