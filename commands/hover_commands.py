from commands.abstract_handlers import CommandFamilyHandler
from commands.abstract_commands import CommandFamily, UIElementCommand
from abc import ABC
from constants.debug_prints import debug_print, DebugStates
from constants.enums import TargetPriority
from commands.scene_manager_protocols import SceneProtocol


class HoverCommandFamily(CommandFamily, UIElementCommand, ABC): pass
class StartHover(HoverCommandFamily): pass
class KeepHover(HoverCommandFamily): pass
class EndHover(HoverCommandFamily): pass


class HoverHandler(CommandFamilyHandler):
    command_type = HoverCommandFamily
    def handler_func(self, command, scene: SceneProtocol):
        command: HoverCommandFamily
        element = command.get_element()
        debug_print(DebugStates.HOVER, command.text, element, scene)
        if isinstance(command, StartHover):
            scene.set_target(element, TargetPriority.HOVER)
        elif isinstance(command, KeepHover):
            scene.keep_target(element, TargetPriority.HOVER)
        elif isinstance(command, EndHover):
            scene.clear_target(element, TargetPriority.HOVER)
