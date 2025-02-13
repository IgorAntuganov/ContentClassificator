from UI_scene.scene import Scene
from commands.trivial_commands import SaveUICommand
from handlers.abstract_handlers import CommandHandler


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
