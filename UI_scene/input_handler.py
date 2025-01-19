import pygame
from constants.states import MouseWheelState

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
