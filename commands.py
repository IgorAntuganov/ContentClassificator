class TextCommand:
    def __init__(self, text):
        self.text = text

    def __eq__(self, other):
        return self.text == other.text


ExitCommand = TextCommand('EXIT')

StartFocus = TextCommand('START_FOCUS')
KeepFocus = TextCommand('KEEP_FOCUS')
EndFocus = TextCommand('END_FOCUS')
