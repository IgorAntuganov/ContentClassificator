from abc import abstractmethod, ABC
import commands
import UI_scene
from constants import debug_print


class CommandHandler(ABC):
    @property
    @abstractmethod
    def command_type(self):
        pass

    def handle(self, command: commands.BaseCommand, scene: UI_scene.Scene):
        if not isinstance(command, self.command_type):
            raise TypeError(f"Expected command of type {self.command_type}, got {type(command)}")
        self.handler_func(command, scene)

    @abstractmethod
    def handler_func(self, command: commands.BaseCommand, scene: UI_scene.Scene):
        pass


class CommandFamilyHandler(CommandHandler, ABC):
    pass


# To do: auto register to manager
class ExitHandler(CommandHandler):  # Handlers classes ----------------
    command_type = commands.ExitCommand
    def handler_func(self, command: commands.ExitCommand, scene: UI_scene.Scene):
        print('Exit Command')
        exit()


class FocusHandler(CommandFamilyHandler):
    command_type = commands.FocusCommandFamily
    def handler_func(self, command: commands.FocusCommandFamily, scene: UI_scene.Scene):
        debug_print('Focus?', command.text, command.get_element(), scene)
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

        if isinstance(command, commands.StartFocus):
            if now_focus is not None:
                raise new_element_error
            scene.set_focused_element(element)
        elif isinstance(command, commands.KeepFocus):
            if now_focus is None:
                raise keep_focus_none_error
            if now_focus is not element:
                raise keep_focus_another_error
        elif isinstance(command, commands.EndFocus):
            if now_focus is not element:
                raise end_focus_error
            scene.clear_focused_element()
        else:
            raise strange_error

        debug_print('focused element:', scene.get_focused_element())


class TestCommandHandler(CommandHandler):
    command_type = commands.TestCommand
    def handler_func(self, command, scene):
        print('get TestCommand')