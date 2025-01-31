from commands.abstract_commands import SceneElementCommand
from abc import ABC


class HoverCommandFamily(SceneElementCommand, ABC): pass # noqa
class StartHover(HoverCommandFamily): pass # noqa
class KeepHover(HoverCommandFamily): pass # noqa
class EndHover(HoverCommandFamily): pass # noqa


class DraggingCommandFamily(SceneElementCommand, ABC): pass # noqa
class StartDragging(DraggingCommandFamily): pass # noqa
class KeepDragging(DraggingCommandFamily): pass # noqa
class EndDragging(DraggingCommandFamily): pass # noqa


class CursorCommandFamily(SceneElementCommand, ABC): pass # noqa
class ClearCursor(CursorCommandFamily): pass # noqa
class DraggingCursor(CursorCommandFamily): pass # noqa
class ErrorCursor(CursorCommandFamily): pass # noqa
