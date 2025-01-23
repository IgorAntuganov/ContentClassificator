from handlers.abstract_handlers import CommandHandler

from constants.debug_prints import DebugStates, debug_print
from constants.enums import TargetPriority
from commands.dragging_commands import DraggingCommandFamily, StartDragging, KeepDragging, EndDragging
from UI_scene.scene import Scene


class DraggingHandler(CommandHandler):
    command_type = DraggingCommandFamily
    def handler_func(self, command: DraggingCommandFamily):
        element = command.get_element()
        scene: Scene = command.get_scene()
        debug_print(DebugStates.DRAGGING, command.text, element, scene)

        if isinstance(command, StartDragging):
            scene.set_target(element, TargetPriority.DRAGGING)
        elif isinstance(command, KeepDragging):
            scene.keep_target(element, TargetPriority.DRAGGING)
        elif isinstance(command, EndDragging):
            scene.clear_target(element, TargetPriority.DRAGGING)
        else:
            raise AssertionError
