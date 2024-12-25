from commands.abstract_handlers import CommandFamilyHandler
from commands.abstract_commands import CommandFamily, UIElementCommand
from abc import ABC
from constants.debug_prints import dragging_debug_print


class DraggingCommandFamily(CommandFamily, UIElementCommand, ABC): pass
class StartDragging(DraggingCommandFamily): pass
class KeepDragging(DraggingCommandFamily): pass
class EndDragging(DraggingCommandFamily): pass


class DraggingHandler(CommandFamilyHandler):
    command_type = DraggingCommandFamily
    def handler_func(self, command, scene):
        command: DraggingCommandFamily
        dragging_debug_print('Dragging?', command.text, command.get_element(), scene)
        element = command.get_element()
        now_focus = scene.get_dragging_element()

        error_info = f'\nNew element: {element}, Old element: {now_focus}, Scene: {scene}'
        new_element_error = ValueError(f'Trying to drag new element when old is still dragging:' + error_info)
        keep_focus_none_error = ValueError(f'Trying to keep dragging element when focused '
                                           f'element is not defined:' + error_info)
        keep_focus_another_error = ValueError(f'Trying to keep dragging an element that is not an element that'
                                              f'is currently defined:' + error_info)
        end_focus_error = ValueError(f'Trying to end dragging an element that is not '
                                     f'an element that is currently defined:' + error_info)
        strange_error = TypeError('IDK, strange command in DraggingHandler:', command)

        if isinstance(command, StartDragging):
            if now_focus is not None:
                raise new_element_error
            scene.set_dragging_element(element)
        elif isinstance(command, KeepDragging):
            if now_focus is None:
                raise keep_focus_none_error
            if now_focus is not element:
                raise keep_focus_another_error
        elif isinstance(command, EndDragging):
            if now_focus is not element:
                raise end_focus_error
            scene.clear_dragging_element()
        else:
            raise strange_error

        dragging_debug_print('dragging element:', scene.get_dragging_element())
