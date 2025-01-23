import pygame

from commands.abstract_commands import base_command_alias
from constants.configs import MouseConfig, create_empty_mouse_config
from constants.enums import MouseWheelState
from commands.trivial_commands import ExitCommand, SaveUICommand


def get_ctrl_alt_shift_array() -> tuple[bool, bool, bool]:
    keys = pygame.key.get_pressed()
    ctrl_pressed = keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]
    alt_pressed = keys[pygame.K_LALT] or keys[pygame.K_RALT]
    shift_pressed = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
    return ctrl_pressed, alt_pressed, shift_pressed


def update_mouse_wheel_state(mws: MouseWheelState, event: pygame.event.Event) -> MouseWheelState:
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 4:
            mws = MouseWheelState.UP
        elif event.button == 5:
            mws = MouseWheelState.DOWN
    return mws


class InputHandler:
    def __init__(self):
        self.event_config: MouseConfig = create_empty_mouse_config()
        self.commands_lst: list[base_command_alias] = []

    def process_tick_events(self):
        self.commands_lst = []

        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        ctrl_alt_shift_array = get_ctrl_alt_shift_array()
        frame_events = pygame.event.get()
        mouse_wheel_state = MouseWheelState.INACTIVE

        for event in frame_events:
            mouse_wheel_state = update_mouse_wheel_state(mouse_wheel_state, event)
            if event.type == pygame.QUIT:
                self.commands_lst.append(ExitCommand())
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.commands_lst.append(ExitCommand())
                if event.key == pygame.K_s:
                    self.commands_lst.append(SaveUICommand())

        self.event_config = MouseConfig(mouse_pos, mouse_pressed, mouse_wheel_state, ctrl_alt_shift_array)

    def get_mouse_config(self) -> MouseConfig:
        return self.event_config

    def get_commands(self) -> list[base_command_alias]:
        return self.commands_lst
