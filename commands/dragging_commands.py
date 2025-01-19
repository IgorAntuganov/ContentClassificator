from commands.abstract_handlers import CommandFamilyHandler
from commands.abstract_commands import CommandFamily, UIElementCommand
from abc import ABC
from constants.debug_prints import DebugStates, debug_print
from constants.states import TargetPriority


class DraggingCommandFamily(CommandFamily, UIElementCommand, ABC): pass
class StartDragging(DraggingCommandFamily): pass
class KeepDragging(DraggingCommandFamily): pass
class EndDragging(DraggingCommandFamily): pass


class DraggingHandler(CommandFamilyHandler):
    command_type = DraggingCommandFamily
    def handler_func(self, command, scene):
        command: DraggingCommandFamily
        debug_print(DebugStates.DRAGGING, command.text, command.get_element(), scene)
        element = command.get_element()
        if isinstance(command, StartDragging):
            scene.set_target(element, TargetPriority.DRAGGING)
        elif isinstance(command, KeepDragging):
            scene.keep_target(element, TargetPriority.DRAGGING)
        elif isinstance(command, EndDragging):
            scene.clear_target(element, TargetPriority.DRAGGING)
