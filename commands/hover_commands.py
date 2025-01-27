from commands.abstract_commands import SceneElementCommand
from abc import ABC


class HoverCommandFamily(SceneElementCommand, ABC): pass
class StartHover(HoverCommandFamily): pass
class KeepHover(HoverCommandFamily): pass
class EndHover(HoverCommandFamily): pass
