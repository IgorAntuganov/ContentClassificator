from abc import abstractmethod, ABC
import commands.command_classes as com_classes
from commands.scene_manager_protocols import SceneProtocol
from constants import debug_print_1, debug_print


class CommandHandler(ABC):
    @property
    @abstractmethod
    def command_type(self):
        pass

    def handle(self, command: com_classes.BaseCommand, scene: SceneProtocol):
        if not isinstance(command, self.command_type):
            raise TypeError(f"Expected command of type {self.command_type}, got {type(command)}")
        self.handler_func(command, scene)

    @abstractmethod
    def handler_func(self, command: com_classes.BaseCommand, scene: SceneProtocol):
        pass


class CommandFamilyHandler(CommandHandler, ABC):
    pass


# To do: auto register to manager
class ExitHandler(CommandHandler):  # Handlers classes ----------------
    command_type = com_classes.ExitCommand
    def handler_func(self, command, scene):
        print('Exit Command')
        exit()

class TestCommandHandler(CommandHandler):
    command_type = com_classes.TestCommand
    def handler_func(self, command, scene):
        print('get TestCommand')

class TestCommandHandler2(CommandHandler):
    command_type = com_classes.TestCommand2
    def handler_func(self, command, scene):
        print('get TestCommand (2!!)')

class SaveUIHandler(CommandHandler):
    command_type = com_classes.SaveUICommand
    def handler_func(self, command, scene):
        scene.save_elements()
        print('UI saved')


class FocusHandler(CommandFamilyHandler):
    command_type = com_classes.DraggingCommandFamily
    def handler_func(self, command, scene):
        command: com_classes.DraggingCommandFamily
        debug_print_1('Focus?', command.text, command.get_element(), scene)
        element = command.get_element()
        now_focus = scene.get_focused_element()

        error_info = f'\nNew element: {element}, Old element: {now_focus}, Scene: {scene}'
        new_element_error = ValueError(f'Trying to focus new element when old is still in focus:' + error_info)
        keep_focus_none_error = ValueError(f'Trying to keep focus element when focused '
                                           f'element is not defined:' + error_info)
        keep_focus_another_error = ValueError(f'Trying to keep in focus an element that is not an element that'
                                              f'is currently defined:' + error_info)
        end_focus_error = ValueError(f'Trying to end focusing an element that is not '
                                     f'an element that is currently defined:' + error_info)
        strange_error = TypeError('IDK, strange command in FocusHandler:', command)

        if isinstance(command, com_classes.StartDragging):
            if now_focus is not None:
                raise new_element_error
            scene.set_focused_element(element)
        elif isinstance(command, com_classes.KeepDragging):
            if now_focus is None:
                raise keep_focus_none_error
            if now_focus is not element:
                raise keep_focus_another_error
        elif isinstance(command, com_classes.EndDragging):
            if now_focus is not element:
                raise end_focus_error
            scene.clear_focused_element()
        else:
            raise strange_error

        debug_print_1('dragging element:', scene.get_focused_element())


class HoverHandler(CommandFamilyHandler):
    command_type = com_classes.HoverCommandFamily
    def handler_func(self, command, scene):
        command: com_classes.HoverCommandFamily
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

        if isinstance(command, com_classes.StartDragging):
            if now_hover is not None:
                raise new_element_error
            scene.set_hovered_element(element)
        elif isinstance(command, com_classes.KeepDragging):
            if now_hover is None:
                raise keep_hover_none_error
            if now_hover is not element:
                raise keep_hover_another_error
        elif isinstance(command, com_classes.EndDragging):
            if now_hover is not element:
                raise end_hover_error
            scene.clear_hovered_element()
        else:
            raise strange_error

        debug_print_1('hovered element:', scene.get_hovered_element())
