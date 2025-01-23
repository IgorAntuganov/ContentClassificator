from abc import ABC, abstractmethod


class AbstractCommand(ABC):
    def __init__(self):
        self._element = None
        self._scene = None

    @property
    def text(self):
        return self.__class__.__name__


    @property
    @abstractmethod
    def need_element(self) -> bool:
        pass

    @property
    @abstractmethod
    def need_scene(self) -> bool:
        pass


    def set_element(self, element):
        self._element = element

    def get_element(self):
        return self._element

    def set_scene(self, scene):
        self._scene = scene

    def get_scene(self):
        return self._scene


class SimpleCommand(AbstractCommand, ABC):
    @property
    def need_element(self) -> bool:
        return False

    @property
    def need_scene(self) -> bool:
        return False


class ElementCommand(AbstractCommand, ABC):
    @property
    def need_element(self) -> bool:
        return True

    @property
    def need_scene(self) -> bool:
        return False


class SceneCommand(AbstractCommand, ABC):
    @property
    def need_element(self) -> bool:
        return True

    @property
    def need_scene(self) -> bool:
        return True


BASE_COMMAND_TYPES = (SimpleCommand, SceneCommand, ElementCommand)
