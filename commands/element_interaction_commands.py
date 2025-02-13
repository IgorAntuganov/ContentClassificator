from commands.abstract_commands import SceneElementCommand
from abc import ABC


class HoverCommandFamily(SceneElementCommand, ABC): pass # noqa
class StartHover(HoverCommandFamily): pass # noqa
class ContinueHover(HoverCommandFamily): pass # noqa
class StopHover(HoverCommandFamily): pass # noqa


class DraggingCommandFamily(SceneElementCommand, ABC): pass # noqa
class StartDrag(DraggingCommandFamily): pass # noqa
class ContinueDrag(DraggingCommandFamily): pass # noqa
class StopDrag(DraggingCommandFamily): pass # noqa


class CursorCommandFamily(SceneElementCommand, ABC): pass # noqa
class ClearCursor(CursorCommandFamily): pass # noqa
class DraggingCursor(CursorCommandFamily): pass # noqa
class ErrorCursor(CursorCommandFamily): pass # noqa
