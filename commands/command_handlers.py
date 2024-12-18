from abc import abstractmethod, ABC
import commands.command_classes as com_classes
from commands.scene_manager_protocols import SceneProtocol


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
