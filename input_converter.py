import pygame
import pyperclip

from constants.configs import EventConfig, SimulatedScancodeWrapper
from constants.enums import MouseWheelState


def get_clipboard_text() -> str | None:
    text = pyperclip.paste()
    if isinstance(text, str) and text.strip():
        return text


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


class InputConverter:
    def __init__(self):
        self.event_config: EventConfig | None = None
        self._is_pygame_quit: bool = False

    def process_tick_events(self) -> EventConfig:
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        ctrl_alt_shift_array = get_ctrl_alt_shift_array()
        mouse_wheel_state = MouseWheelState.INACTIVE

        keys_pressed = pygame.key.get_pressed()
        keys_just_pressed = SimulatedScancodeWrapper()
        keys_just_released = SimulatedScancodeWrapper()
        unicodes_just_pressed = SimulatedScancodeWrapper()
        unicodes_just_released = SimulatedScancodeWrapper()

        pasted_text = None
        for event in pygame.event.get():
            mouse_wheel_state = update_mouse_wheel_state(mouse_wheel_state, event)

            if event.type == pygame.QUIT:
                self._is_pygame_quit = True
            if event.type == pygame.KEYDOWN:
                keys_just_pressed.add(event.key)
                unicodes_just_pressed.add(event.unicode)
                if event.key == pygame.K_v and (event.mod & pygame.KMOD_CTRL):
                    pasted_text = get_clipboard_text()
            if event.type == pygame.KEYUP:
                unicodes_just_released.add(event.unicode)
                keys_just_released.add(event.key)

        self.event_config = EventConfig(mouse_pos, mouse_pressed, mouse_wheel_state, ctrl_alt_shift_array,
                                        keys_pressed, keys_just_pressed, keys_just_released,
                                        unicodes_just_pressed, unicodes_just_released, pasted_text)
        return self.event_config

    def is_pygame_quit(self) -> bool:
        return self._is_pygame_quit
