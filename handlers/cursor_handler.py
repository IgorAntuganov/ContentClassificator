from UI_scene.scene_class import Scene
from handlers.abstract_handlers import CommandHandler
from constants.debug_prints import DebugStates, debug_print
from commands.element_interaction_commands import CursorCommandFamily, ClearCursor, DraggingCursor, ErrorCursor


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
