class Command:
    pass


class TextCommand(Command):
    def __init__(self, text):
        self.text = text
