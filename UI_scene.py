import pygame
from UI_abstracts import BaseUIElement, MouseConfig
from states import MouseWheelState
from commands import BaseCommand, ExitCommand


class Scene:
    def __init__(self, name: str, elements: list[BaseUIElement]):
        self.name = name
        self.elements: list[BaseUIElement] = elements
        self._focused_element: BaseUIElement | None = None

    def set_focused_element(self, element: BaseUIElement):
        self._focused_element = element

    def get_focused_element(self) -> BaseUIElement:
        return self._focused_element

    def handle_events(self) -> list[BaseCommand]:
        commands_pool = []

        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        ctrl_alt_shift_array = self.get_ctrl_alt_shift_array()
        frame_events = pygame.event.get()
        mouse_wheel_state = MouseWheelState.INACTIVE

        for event in frame_events:
            mouse_wheel_state = self.update_mouse_wheel_state(mouse_wheel_state, event)
            if event.type == pygame.QUIT:
                commands_pool.append(ExitCommand())
                return commands_pool
            if event.type == pygame.KEYDOWN:
                # if event.key == pygame.K_s:
                #     commands_pool.append(BaseCommand('SAVE_UI'))
                # if event.key == pygame.K_d:
                #     commands_pool.append(BaseCommand('NEXT_IMAGE'))
                pass

        event_config = MouseConfig(mouse_pos, mouse_pressed, mouse_wheel_state, ctrl_alt_shift_array)
        for el in self.elements:
            new_commands = el.handle_mouse(event_config)
            commands_pool += new_commands

        return commands_pool

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
