from handlers.abstract_handlers import CommandHandler

from constants.debug_prints import DebugStates, debug_print
from constants.enums import TargetPriority
from commands.element_interaction_commands import DraggingCommandFamily, StartDrag, ContinueDrag, StopDrag
from UI_scene.scene_class import Scene


class DraggingHandler(CommandHandler):
    command_type = DraggingCommandFamily

    def handler_func(self, command):
        assert isinstance(command, DraggingCommandFamily)
        element = command.get_element()
        scene: Scene = command.get_scene()
        debug_print(DebugStates.DRAGGING, command.text, element, scene)

        if isinstance(command, StartDrag):
            scene.set_target(element, TargetPriority.DRAGGING)
        elif isinstance(command, ContinueDrag):
            scene.keep_target(element, TargetPriority.DRAGGING)
        elif isinstance(command, StopDrag):
            scene.clear_target(element, TargetPriority.DRAGGING)
        else:
            raise AssertionError
