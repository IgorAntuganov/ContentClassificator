from commands.abstract_commands import SceneCommand
from abc import ABC


class CursorCommandFamily(SceneCommand, ABC): pass
class ClearCursor(CursorCommandFamily): pass
class DraggingCursor(CursorCommandFamily): pass
class ErrorCursor(CursorCommandFamily): pass
