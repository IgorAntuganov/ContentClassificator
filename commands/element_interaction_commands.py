from commands.abstract_commands import SceneElementCommand
from abc import ABC


class HoverCommandFamily(SceneElementCommand, ABC): pass
class StartHover(HoverCommandFamily): pass
class KeepHover(HoverCommandFamily): pass
class EndHover(HoverCommandFamily): pass


class DraggingCommandFamily(SceneElementCommand, ABC): pass
class StartDragging(DraggingCommandFamily): pass
class KeepDragging(DraggingCommandFamily): pass
class EndDragging(DraggingCommandFamily): pass


class CursorCommandFamily(SceneElementCommand, ABC): pass
class ClearCursor(CursorCommandFamily): pass
class DraggingCursor(CursorCommandFamily): pass
class ErrorCursor(CursorCommandFamily): pass
