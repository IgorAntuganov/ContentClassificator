from commands.hover_commands import StartHover, KeepHover, EndHover, HoverCommandFamily
from constants.debug_prints import debug_print, DebugStates
from constants.enums import TargetPriority
from handlers.abstract_handlers import CommandHandler
from UI_scene.scene import Scene


class HoverHandler(CommandHandler):
    command_type = HoverCommandFamily
    def handler_func(self, command):
        assert isinstance(command, HoverCommandFamily)
        element = command.get_element()
        scene: Scene = command.get_scene()
        debug_print(DebugStates.HOVER, command.text, element, scene)

        if isinstance(command, StartHover):
            scene.set_target(element, TargetPriority.HOVER)
        elif isinstance(command, KeepHover):
            scene.keep_target(element, TargetPriority.HOVER)
        elif isinstance(command, EndHover):
            scene.clear_target(element, TargetPriority.HOVER)
        else:
            raise AssertionError