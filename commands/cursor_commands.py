from commands.abstract_commands import SceneElementCommand
from abc import ABC


class CursorCommandFamily(SceneElementCommand, ABC): pass
class ClearCursor(CursorCommandFamily): pass
class DraggingCursor(CursorCommandFamily): pass
class ErrorCursor(CursorCommandFamily): pass
