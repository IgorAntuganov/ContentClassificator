from commands.abstract_commands import SimpleCommand, SceneCommand


class ExitCommand(SimpleCommand):
    text = 'Exit'
class TestCommand(SimpleCommand):
    text = 'Test'
class TestCommand2(SimpleCommand):
    text = 'Test_2'
class SaveUICommand(SceneCommand):
    text = 'Save_UI'
