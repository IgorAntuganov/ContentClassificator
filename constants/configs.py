from dataclasses import dataclass
from constants.states import MouseWheelState

@dataclass
class MouseConfig:
    mouse_position: tuple[int, int]
    mouse_pressed: tuple[bool, bool, bool]
    mouse_wheel_state: MouseWheelState
    ctrl_alt_shift_array: tuple[bool, bool, bool]
