from dataclasses import dataclass
from constants.enums import MouseWheelState

@dataclass
class MouseConfig:
    mouse_position: tuple[int, int]
    mouse_pressed: tuple[bool, bool, bool]
    mouse_wheel_state: MouseWheelState
    ctrl_alt_shift_array: tuple[bool, bool, bool]


def create_empty_mouse_config() -> MouseConfig:
    return MouseConfig((0, 0), (False,)*3, MouseWheelState.INACTIVE, (False,)*3)

