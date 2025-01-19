import pygame

from UI_elements import UI_abstracts
from UI_elements.abstract_element import AbstractUIElement
from constants.states import MouseWheelState, TargetPriority
from commands.abstract_commands import BaseCommand
from commands.trivial_commands import ExitCommand, SaveUICommand
from commands.scene_manager_protocols import ManagerProtocol
from cursor_manager import CursorManager

import UI_scene.input_handler as inp_handler
from UI_scene.elements_collections import SceneElements, SceneElementsManager


class Scene:
    def __init__(self, name: str, elements: list[AbstractUIElement], scene_commands_manager: ManagerProtocol):
        self.name = name
        self.tick = 0
        self.last_target_tick = self.tick

        self._elements: SceneElements = SceneElements(elements, set(elements))
        self._elements_manager = SceneElementsManager(self._elements)

        self._scene_commands_manager = scene_commands_manager
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

    def handle_events(self) -> list[BaseCommand]:
        self.tick += 1
        assert self.tick-1 == self.last_target_tick
        if self._elements_manager.get_targeted_element() is None:
            self.last_target_tick = self.tick

        not_scene_commands: list[BaseCommand] = []

        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        ctrl_alt_shift_array = inp_handler.get_ctrl_alt_shift_array()
        frame_events = pygame.event.get()
        mouse_wheel_state = MouseWheelState.INACTIVE

        for event in frame_events:
            mouse_wheel_state = inp_handler.update_mouse_wheel_state(mouse_wheel_state, event)
            if event.type == pygame.QUIT:
                not_scene_commands.append(ExitCommand())
                return not_scene_commands
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    not_scene_commands.append(ExitCommand())
                    return not_scene_commands
                if event.key == pygame.K_s:
                    self._scene_commands_manager.handle_command(SaveUICommand())

        event_config = UI_abstracts.MouseConfig(mouse_pos, mouse_pressed, mouse_wheel_state, ctrl_alt_shift_array)

        if self._elements_manager.is_dragging:
            dragging_element = self._elements_manager.get_targeted_element()
            element_commands = dragging_element.handle_mouse(event_config)
            not_scene_commands += self._scene_commands_manager.filter_non_handleable(element_commands)
            scene_commands = self._scene_commands_manager.filter_handleable(element_commands)
            self._scene_commands_manager.handle_commands(scene_commands)
            return not_scene_commands

        if self._elements_manager.is_hovering:
            hovered_element = self._elements_manager.get_targeted_element()
            element_commands = hovered_element.handle_mouse(event_config)
            not_scene_commands += self._scene_commands_manager.filter_non_handleable(element_commands)
            scene_commands = self._scene_commands_manager.filter_handleable(element_commands)
            self._scene_commands_manager.handle_commands(scene_commands)
            return not_scene_commands

        for el in self._elements_manager.get_ordered_elements():
            element_commands = el.handle_mouse(event_config)
            not_scene_commands += self._scene_commands_manager.filter_non_handleable(element_commands)
            scene_commands = self._scene_commands_manager.filter_handleable(element_commands)
            self._scene_commands_manager.handle_commands(scene_commands)
            if self._elements_manager.get_targeted_element() is not None:
                break

        return not_scene_commands

    def draw_elements(self, screen: pygame.Surface):
        for el in self._elements_manager.get_ordered_elements():
            el.draw(screen)

    def save_elements(self):
        for el in self._elements_manager.get_ordered_elements():
            assert isinstance(el, UI_abstracts.JSONadjustable)
            el.save_to_json()
