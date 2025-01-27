from commands.abstract_commands import SceneElementCommand
from abc import ABC


class DraggingCommandFamily(SceneElementCommand, ABC): pass
class StartDragging(DraggingCommandFamily): pass
class KeepDragging(DraggingCommandFamily): pass
class EndDragging(DraggingCommandFamily): pass
