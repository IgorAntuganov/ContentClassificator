from UI_scene.scene_class import Scene
from handlers.abstract_handlers import CommandHandler
from constants.enums import TargetPriority
from constants.debug_prints import DebugStates, debug_print

from commands.element_interaction_commands import CursorCommandFamily, ClearCursor, DraggingCursor, ErrorCursor
from commands.element_interaction_commands import DraggingCommandFamily, StartDrag, ContinueDrag, StopDrag
from commands.element_interaction_commands import StartHover, ContinueHover, StopHover, HoverCommandFamily
from commands.trivial_commands import SaveUICommand


class CursorHandler(CommandHandler):
    command_type = CursorCommandFamily

    def handler_func(self, command):
        assert isinstance(command, CursorCommandFamily)
        scene: Scene = command.get_scene()
        debug_print(DebugStates.CURSOR, command.text, command.get_element(), scene)
        _cursor_manager = scene.get_cursor_manager()

        if isinstance(command, ClearCursor):
            _cursor_manager.clear_cursor()
        elif isinstance(command, DraggingCursor):
            # noinspection SpellCheckingInspection
            cursor_key = 'sizeall'  # PyCharm marking this pygame element as typo
            _cursor_manager.set_cursor(cursor_key)
        elif isinstance(command, ErrorCursor):
            cursor_key = 'no'
            _cursor_manager.set_cursor(cursor_key)
        else:
            raise AssertionError

        debug_print(DebugStates.CURSOR, 'now cursor:', _cursor_manager.get_current_cursor())


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


class HoverHandler(CommandHandler):
    command_type = HoverCommandFamily

    def handler_func(self, command):
        assert isinstance(command, HoverCommandFamily)
        element = command.get_element()
        scene: Scene = command.get_scene()
        debug_print(DebugStates.HOVER, command.text, element, scene)

        if isinstance(command, StartHover):
            scene.set_target(element, TargetPriority.HOVER)
        elif isinstance(command, ContinueHover):
            scene.keep_target(element, TargetPriority.HOVER)
        elif isinstance(command, StopHover):
            scene.clear_target(element, TargetPriority.HOVER)
        else:
            raise AssertionError


class SaveUIHandler(CommandHandler):
    command_type = SaveUICommand

    def handler_func(self, command):
        assert isinstance(command, SaveUICommand)
        scene = command.get_scene()
        assert isinstance(scene, Scene)
        save_manager = scene.get_save_manager()
        elements = scene.get_elements_manager().elements_dct
        save_manager.save_elements(elements)
        print('UI saved')
