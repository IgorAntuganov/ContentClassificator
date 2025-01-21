import pygame

from UI_elements.abstract_element import AbstractUIElement
from constants.enums import TargetPriority
from commands.abstract_commands import BaseCommand, SceneCommand
from commands.command_manager import CommandHandlerManager
from cursor_manager import CursorManager

import UI_scene.input_handler as inp_handler
from UI_scene.elements_collections import SceneElements, SceneElementsManager


class Scene:
    def __init__(self, name: str, elements: list[AbstractUIElement], scene_commands_manager: CommandHandlerManager):
        self.name = name
        self.tick = 0
        self.last_target_tick = self.tick

        self._elements: SceneElements = SceneElements(elements, set(elements))
        self._elements_manager = SceneElementsManager(self._elements)

        self._commands_manager = scene_commands_manager
        self._input_handler = inp_handler.InputHandler()
        self._cursor_manager: CursorManager = CursorManager()

    def get_elements_manager(self) -> SceneElementsManager:
        return self._elements_manager

    def get_cursor_manager(self) -> CursorManager:
        return self._cursor_manager


    def set_target(self, element: AbstractUIElement, priority: TargetPriority):
        self._elements_manager.set_interation_element(element, priority)
        self.last_target_tick = self.tick

    def keep_target(self, element: AbstractUIElement, priority: TargetPriority):
        assert self._elements_manager.is_element_targeted(element, priority)
        self.last_target_tick = self.tick

    def clear_target(self, element: AbstractUIElement, priority: TargetPriority):
        self._elements_manager.clear_interation_element(element, priority)
        self.last_target_tick = self.tick


    def filter_and_handle_unsorted(self, commands_lst: list[BaseCommand]) -> list[BaseCommand]:
        for command in commands_lst:
            if isinstance(command, SceneCommand):
                command.set_scene(self)
        non_handleable = self._commands_manager.filter_non_handleable(commands_lst)
        scene_commands = self._commands_manager.filter_handleable(commands_lst)
        self._commands_manager.handle_commands(scene_commands)
        return non_handleable

    def handle_events(self) -> list[BaseCommand]:
        self.tick += 1
        assert self.tick-1 == self.last_target_tick
        if self._elements_manager.get_targeted_element() is None:
            self.last_target_tick = self.tick

        not_scene_commands: list[BaseCommand] = []

        self._input_handler.process_tick_events()
        event_config = self._input_handler.get_mouse_config()

        commands_from_input = self._input_handler.get_commands()
        not_scene_commands += self.filter_and_handle_unsorted(commands_from_input)

        if self._elements_manager.is_dragging:
            dragging_element = self._elements_manager.get_targeted_element()
            element_commands = dragging_element.handle_mouse(event_config)
            not_scene_commands += self.filter_and_handle_unsorted(element_commands)
            return not_scene_commands

        if self._elements_manager.is_hovering:
            hovered_element = self._elements_manager.get_targeted_element()
            element_commands = hovered_element.handle_mouse(event_config)
            not_scene_commands += self.filter_and_handle_unsorted(element_commands)
            return not_scene_commands

        for el in self._elements_manager.get_ordered_elements():
            element_commands = el.handle_mouse(event_config)
            not_scene_commands += self.filter_and_handle_unsorted(element_commands)
            if self._elements_manager.get_targeted_element() is not None:
                break

        return not_scene_commands

    def draw_elements(self, screen: pygame.Surface):
        for el in self._elements_manager.get_ordered_elements():
            el.draw(screen)
