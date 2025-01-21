from commands.abstract_handlers import CommandFamilyHandler
from commands.abstract_commands import CommandFamily, UIElementCommand
from abc import ABC

from commands.scene_manager_protocols import SceneProtocol
from constants.debug_prints import DebugStates, debug_print
from constants.enums import TargetPriority


class DraggingCommandFamily(CommandFamily, UIElementCommand, ABC): pass
class StartDragging(DraggingCommandFamily): pass
class KeepDragging(DraggingCommandFamily): pass
class EndDragging(DraggingCommandFamily): pass


class DraggingHandler(CommandFamilyHandler):
    command_type = DraggingCommandFamily
    def handler_func(self, command: DraggingCommandFamily):
        scene: SceneProtocol
        element = command.get_element()
        scene = command.get_scene()
        debug_print(DebugStates.DRAGGING, command.text, element, scene)

        if isinstance(command, StartDragging):
            scene.set_target(element, TargetPriority.DRAGGING)
        elif isinstance(command, KeepDragging):
            scene.keep_target(element, TargetPriority.DRAGGING)
        elif isinstance(command, EndDragging):
            scene.clear_target(element, TargetPriority.DRAGGING)
