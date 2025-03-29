from abc import ABC, abstractmethod
from UI_scene.scene_class import Scene
from handlers.command_manager import CommandHandlerManager


class SceneCreator(ABC):
    @abstractmethod
    def get_scene_and_manager(self) -> tuple[Scene, CommandHandlerManager]:
        pass
