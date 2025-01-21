from commands.abstract_handlers import CommandFamilyHandler
from commands.abstract_commands import CommandFamily, UIElementCommand
from abc import ABC
from constants.debug_prints import DebugStates, debug_print


class CursorCommandFamily(CommandFamily, UIElementCommand, ABC): pass
class ClearCursor(CursorCommandFamily): pass
class DraggingCursor(CursorCommandFamily): pass
class ErrorCursor(CursorCommandFamily): pass


class CursorHandler(CommandFamilyHandler):
    command_type = CursorCommandFamily
    def handler_func(self, command):
        command: CursorCommandFamily
        scene = command.get_scene()
        debug_print(DebugStates.CURSOR, command.text, command.get_element(), scene)
        _cursor_manager = scene.get_cursor_manager()

        strange_error = TypeError('IDK, strange command in CursorHandler:', command)

        if isinstance(command, ClearCursor):
            _cursor_manager.clear_cursor()
        elif isinstance(command, DraggingCursor):
            cursor_key = 'sizeall'
            _cursor_manager.set_cursor(cursor_key)
        elif isinstance(command, ErrorCursor):
            cursor_key = 'no'
            _cursor_manager.set_cursor(cursor_key)
        else:
            raise strange_error

        debug_print(DebugStates.CURSOR, 'now cursor:', _cursor_manager.get_current_cursor())
