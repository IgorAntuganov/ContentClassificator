from commands.command_handlers import CommandFamilyHandler
from commands.command_classes import CommandFamily, UIElementCommand
from abc import ABC
from constants import debug_print_1


class DraggingCommandFamily(CommandFamily, UIElementCommand, ABC): pass
class StartDragging(DraggingCommandFamily): pass
class KeepDragging(DraggingCommandFamily): pass
class EndDragging(DraggingCommandFamily): pass


class DraggingHandler(CommandFamilyHandler):
    command_type = DraggingCommandFamily
    def handler_func(self, command, scene):
        command: DraggingCommandFamily
        debug_print_1('Focus?', command.text, command.get_element(), scene)
        element = command.get_element()
        now_focus = scene.get_dragging_element()

        error_info = f'\nNew element: {element}, Old element: {now_focus}, Scene: {scene}'
        new_element_error = ValueError(f'Trying to focus new element when old is still in focus:' + error_info)
        keep_focus_none_error = ValueError(f'Trying to keep focus element when focused '
                                           f'element is not defined:' + error_info)
        keep_focus_another_error = ValueError(f'Trying to keep in focus an element that is not an element that'
                                              f'is currently defined:' + error_info)
        end_focus_error = ValueError(f'Trying to end focusing an element that is not '
                                     f'an element that is currently defined:' + error_info)
        strange_error = TypeError('IDK, strange command in FocusHandler:', command)

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

        debug_print_1('dragging element:', scene.get_dragging_element())