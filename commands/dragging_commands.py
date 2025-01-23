from commands.abstract_commands import SceneCommand
from abc import ABC


class DraggingCommandFamily(SceneCommand, ABC): pass
class StartDragging(DraggingCommandFamily): pass
class KeepDragging(DraggingCommandFamily): pass
class EndDragging(DraggingCommandFamily): pass
