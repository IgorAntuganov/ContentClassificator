import pygame
from typing import Generator

from UI_elements.abstract_element import UIElement
from constants.configs import EventConfig
from constants.enums import TargetPriority
from commands.abstract_commands import CommandList
from commands.trivial_commands import ExitCommand, SaveUICommand
from UI_scene.cursor_manager import CursorManager

import UI_scene.input_converter as inp_handler
from UI_scene.elements_collections import SceneElements, SceneElementsManager


class Scene:
    def __init__(self, name: str, elements: list[UIElement]):
        self.name = name
        self.tick = 0
        self._last_target_tick = self.tick

        self._elements: SceneElements = SceneElements(elements, set(elements))
        self._elements_manager = SceneElementsManager(self._elements)

        self._input_converter = inp_handler.InputConverter()
        self._cursor_manager: CursorManager = CursorManager()

    def get_elements_manager(self) -> SceneElementsManager:
        return self._elements_manager

    def get_cursor_manager(self) -> CursorManager:
        return self._cursor_manager

    def set_target(self, element: UIElement, priority: TargetPriority):
        self._elements_manager.set_interation_element(element, priority)
        self._last_target_tick = self.tick

    def keep_target(self, element: UIElement, priority: TargetPriority):
        assert self._elements_manager.is_element_targeted(element, priority)
        self._last_target_tick = self.tick

    def clear_target(self, element: UIElement, priority: TargetPriority):
        self._elements_manager.clear_interation_element(element, priority)
        self._last_target_tick = self.tick

    def _add_all_associations(self, command_lst: CommandList, element: UIElement) -> CommandList:
        command_lst = self._add_scene_associations(command_lst)
        for command in command_lst:
            if command.need_element:
                command.set_element(element)
        return command_lst

    def _add_scene_associations(self, command_lst: CommandList) -> CommandList:
        for command in command_lst:
            if command.need_scene:
                command.set_scene(self)
        return command_lst

    @staticmethod
    def _create_scene_commands(config: EventConfig) -> CommandList:
        commands_lst: CommandList = []
        if config.keys_just_pressed[pygame.K_s]:
            commands_lst.append(SaveUICommand())
        if config.keys_just_pressed[pygame.K_ESCAPE]:
            commands_lst.append(ExitCommand())
        return commands_lst

    def handle_events(self) -> Generator[CommandList, None, None]:
        self.tick += 1
        assert self.tick-1 == self._last_target_tick
        if self._elements_manager.get_target() is None:
            self._last_target_tick = self.tick

        self._input_converter.process_tick_events()
        event_config = self._input_converter.get_event_config()

        if self._input_converter.is_pygame_quit():
            yield [ExitCommand()]
        scene_commands = self._create_scene_commands(event_config)
        yield self._add_scene_associations(scene_commands)

        if self._elements_manager.is_dragging:
            dragging_element = self._elements_manager.get_targeted_element()
            element_commands = dragging_element.handle_events(event_config)
            yield self._add_all_associations(element_commands, dragging_element)
            return

        if self._elements_manager.is_hovering:
            hovered_element = self._elements_manager.get_targeted_element()
            element_commands = hovered_element.handle_events(event_config)
            yield self._add_all_associations(element_commands, hovered_element)
            return

        for el in self._elements_manager.get_ordered_elements():
            element_commands = el.handle_events(event_config)
            yield self._add_all_associations(element_commands, el)
            if self._elements_manager.get_target() is not None:
                return
        return

    def draw_elements(self, screen: pygame.Surface):
        for el in self._elements_manager.get_ordered_elements():
            el.draw(screen)
