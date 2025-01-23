import pygame
from typing import Generator

from UI_elements.abstract_element import AbstractUIElement
from constants.enums import TargetPriority
from commands.abstract_commands import BASE_COMMAND_TYPES
from cursor_manager import CursorManager

import UI_scene.input_handler as inp_handler
from UI_scene.elements_collections import SceneElements, SceneElementsManager


class Scene:
    def __init__(self, name: str, elements: list[AbstractUIElement]):
        self.name = name
        self.tick = 0
        self._last_target_tick = self.tick

        self._elements: SceneElements = SceneElements(elements, set(elements))
        self._elements_manager = SceneElementsManager(self._elements)

        self._input_handler = inp_handler.InputHandler()
        self._cursor_manager: CursorManager = CursorManager()

    def get_elements_manager(self) -> SceneElementsManager:
        return self._elements_manager

    def get_cursor_manager(self) -> CursorManager:
        return self._cursor_manager


    def set_target(self, element: AbstractUIElement, priority: TargetPriority):
        self._elements_manager.set_interation_element(element, priority)
        self._last_target_tick = self.tick

    def keep_target(self, element: AbstractUIElement, priority: TargetPriority):
        assert self._elements_manager.is_element_targeted(element, priority)
        self._last_target_tick = self.tick

    def clear_target(self, element: AbstractUIElement, priority: TargetPriority):
        self._elements_manager.clear_interation_element(element, priority)
        self._last_target_tick = self.tick


    def _add_all_associations(self, command_lst: list[BASE_COMMAND_TYPES], element):
        self._add_scene_associations(command_lst)
        for command in command_lst:
            if command.need_element:
                command.set_element(element)

    def _add_scene_associations(self, command_lst: list[BASE_COMMAND_TYPES]):
        for command in command_lst:
            if command.need_scene:
                command.set_scene(self)


    def handle_events(self) -> Generator[list[BASE_COMMAND_TYPES], None, None]:
        self.tick += 1
        assert self.tick-1 == self._last_target_tick
        if self._elements_manager.get_targeted_element() is None:
            self._last_target_tick = self.tick

        self._input_handler.process_tick_events()
        event_config = self._input_handler.get_mouse_config()

        commands_from_input = self._input_handler.get_commands()
        self._add_scene_associations(commands_from_input)
        yield commands_from_input

        if self._elements_manager.is_dragging:
            dragging_element = self._elements_manager.get_targeted_element()
            element_commands = dragging_element.handle_mouse(event_config)
            self._add_all_associations(element_commands, dragging_element)
            yield element_commands
            return

        if self._elements_manager.is_hovering:
            hovered_element = self._elements_manager.get_targeted_element()
            element_commands = hovered_element.handle_mouse(event_config)
            self._add_all_associations(element_commands, hovered_element)
            yield element_commands
            return

        for el in self._elements_manager.get_ordered_elements():
            element_commands = el.handle_mouse(event_config)
            self._add_all_associations(element_commands, el)
            yield element_commands
            if self._elements_manager.get_targeted_element() is not None:
                return
        return

    def draw_elements(self, screen: pygame.Surface):
        for el in self._elements_manager.get_ordered_elements():
            el.draw(screen)
