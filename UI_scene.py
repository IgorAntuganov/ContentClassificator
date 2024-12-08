import pygame
from UI_abstracts import MouseConfig
from UI_element import MetaUIElement
from states import MouseWheelState
from commands import BaseCommand, ExitCommand
from scene_manager_protocols import ManagerProtocol, SceneProtocol


class Scene(SceneProtocol):
    def __init__(self, name: str, elements: list[MetaUIElement], scene_manager: ManagerProtocol):
        self.name = name
        self.elements: list[MetaUIElement] = elements
        self.scene_manager = scene_manager
        self._focused_element: MetaUIElement | None = None

    def set_focused_element(self, element: MetaUIElement):
        if element not in self.elements:
            raise AssertionError(f'Trying to focus element, that not in scene.elements. Element: {element}')
        self._focused_element = element
        self.elements.remove(element)
        self.elements.append(element)

    def get_focused_element(self) -> MetaUIElement | None:
        return self._focused_element

    def clear_focused_element(self):
        self._focused_element = None

    def handle_events(self) -> list[BaseCommand]:
        not_scene_commands: list[BaseCommand] = []

        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        ctrl_alt_shift_array = self.get_ctrl_alt_shift_array()
        frame_events = pygame.event.get()
        mouse_wheel_state = MouseWheelState.INACTIVE

        for event in frame_events:
            mouse_wheel_state = self.update_mouse_wheel_state(mouse_wheel_state, event)
            if event.type == pygame.QUIT:
                not_scene_commands.append(ExitCommand())
                return not_scene_commands
            if event.type == pygame.KEYDOWN:
                # if event.key == pygame.K_s:
                #     not_scene_commands.append(BaseCommand('SAVE_UI'))
                # if event.key == pygame.K_d:
                #     not_scene_commands.append(BaseCommand('NEXT_IMAGE'))
                pass

        event_config = MouseConfig(mouse_pos, mouse_pressed, mouse_wheel_state, ctrl_alt_shift_array)

        if self._focused_element is not None:
            element_commands = self._focused_element.handle_mouse(event_config)
            not_scene_commands += self.scene_manager.filter_non_handleable(element_commands)
            scene_commands = self.scene_manager.filter_handleable(element_commands)
            self.scene_manager.handle_commands(scene_commands)

        element_index = 0
        while self._focused_element is None and element_index < len(self.elements):
            ind = len(self.elements) - element_index - 1
            el = self.elements[ind]
            element_commands = el.handle_mouse(event_config)
            not_scene_commands += self.scene_manager.filter_non_handleable(element_commands)
            scene_commands = self.scene_manager.filter_handleable(element_commands)
            self.scene_manager.handle_commands(scene_commands)
            element_index += 1

        return not_scene_commands

    @staticmethod
    def get_ctrl_alt_shift_array() -> tuple[bool, bool, bool]:
        keys = pygame.key.get_pressed()
        ctrl_pressed = keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]
        alt_pressed = keys[pygame.K_LALT] or keys[pygame.K_RALT]
        shift_pressed = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
        return ctrl_pressed, alt_pressed, shift_pressed

    @staticmethod
    def update_mouse_wheel_state(mws: MouseWheelState, event: pygame.event.Event) -> MouseWheelState:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                mws = MouseWheelState.UP
            elif event.button == 5:
                mws = MouseWheelState.DOWN
        return mws

    def draw_elements(self, screen: pygame.Surface):
        for el in self.elements:
            el.draw(screen)
