from commands.abstract_commands import SceneCommand
from abc import ABC


class HoverCommandFamily(SceneCommand, ABC): pass
class StartHover(HoverCommandFamily): pass
class KeepHover(HoverCommandFamily): pass
class EndHover(HoverCommandFamily): pass
