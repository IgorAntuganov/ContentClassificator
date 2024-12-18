from commands.command_handlers import CommandFamilyHandler
from commands.command_classes import CommandFamily, UIElementCommand
from abc import ABC
from constants import debug_print_1


class HoverCommandFamily(CommandFamily, UIElementCommand, ABC): pass
class StartHover(HoverCommandFamily): pass
class KeepHover(HoverCommandFamily): pass
class EndHover(HoverCommandFamily): pass


class HoverHandler(CommandFamilyHandler):
    command_type = HoverCommandFamily
    def handler_func(self, command, scene):
        command: HoverCommandFamily
        debug_print_1('Hover?', command.text, command.get_element(), scene)
        element = command.get_element()
        now_hover = scene.get_hovered_element()

        error_info = f'\nNew element: {element}, Old element: {now_hover}, Scene: {scene}'
        new_element_error = ValueError(f'Trying to hover new element when old is still in hover:' + error_info)
        keep_hover_none_error = ValueError(f'Trying to keep hover element when hovered '
                                           f'element is not defined:' + error_info)
        keep_hover_another_error = ValueError(f'Trying to keep in hover an element that is not an element that'
                                              f'is currently defined:' + error_info)
        end_hover_error = ValueError(f'Trying to end hovering an element that is not '
                                     f'an element that is currently defined:' + error_info)
        strange_error = TypeError('IDK, strange command in HoverHandler:', command)

        if isinstance(command, StartHover):
            if now_hover is not None:
                raise new_element_error
            scene.set_hovered_element(element)
        elif isinstance(command, KeepHover):
            if now_hover is None:
                raise keep_hover_none_error
            if now_hover is not element:
                raise keep_hover_another_error
        elif isinstance(command, EndHover):
            if now_hover is not element:
                raise end_hover_error
            scene.clear_hovered_element()
        else:
            raise strange_error

        debug_print_1('hovered element:', scene.get_hovered_element())