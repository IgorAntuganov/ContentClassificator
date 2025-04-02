import pygame
from typing import Generator

from UI_elements.abstract_element import UIElement
from constants.configs import EventConfig
from commands.abstract_commands import CommandList
from commands.trivial_commands import ExitCommand, SaveUICommand

from UI_scene.save_manager import SaveManager
from UI_scene.cursor_manager import CursorManager
import input_converter
from UI_scene.focus_manager import FocusManager


class Scene:
    def __init__(self, name: str, elements_dct: dict[str, UIElement]):
        self.name = name

        self._ordered_elements = list(elements_dct.values())
        self._focus_manager = FocusManager(elements_dct)

        self._input_converter = input_converter.InputConverter()
        self._cursor_manager: CursorManager = CursorManager()
        self._save_manager = SaveManager(name)
        self._save_manager.register_and_configure(elements_dct)

    def add_new_element(self, element_name: str, element: UIElement):
        assert element not in self._ordered_elements
        self._ordered_elements.append(element)
        self._focus_manager.add_new_element(element_name, element)

    def get_focus_manager(self) -> FocusManager:
        return self._focus_manager

    def get_cursor_manager(self) -> CursorManager:
        return self._cursor_manager

    def get_save_manager(self) -> SaveManager:
        return self._save_manager

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
        if config.keys_just_pressed[pygame.K_BACKQUOTE]:
            commands_lst.append(SaveUICommand())
        if config.keys_just_pressed[pygame.K_ESCAPE]:
            commands_lst.append(ExitCommand())
        return commands_lst

    def handle_events(self) -> Generator[CommandList, None, None]:
        self._focus_manager.tick()

        event_config = self._input_converter.process_tick_events()
        if self._input_converter.is_pygame_quit():
            yield [ExitCommand()]

        scene_commands = self._create_scene_commands(event_config)
        yield self._add_scene_associations(scene_commands)

        if self._focus_manager.is_dragging:
            dragging_element = self._focus_manager.get_targeted_element()
            element_commands = dragging_element.handle_events(event_config)
            yield self._add_all_associations(element_commands, dragging_element)
            return

        if self._focus_manager.is_hovering:
            hovered_element = self._focus_manager.get_targeted_element()
            element_commands = hovered_element.handle_events(event_config)
            yield self._add_all_associations(element_commands, hovered_element)
            return

        for el in self._ordered_elements:
            element_commands = el.handle_events(event_config)
            yield self._add_all_associations(element_commands, el)
            if self._focus_manager.get_target() is not None:
                return
        return

    def draw_elements(self, screen: pygame.Surface):
        for el in self._ordered_elements:
            el.draw(screen)
