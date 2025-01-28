from dataclasses import dataclass
from pygame.key import ScancodeWrapper
from constants.enums import MouseWheelState


class SimulatedScancodeWrapper:
    def __init__(self):
        self.keys = set()

    def add(self, key: int):
        self.keys.add(key)

    def __contains__(self, key: int) -> bool:
        return key in self.keys

    def __getitem__(self, key: int) -> bool:
        return key in self.keys

    def __repr__(self) -> str:
        return f"JustPressedKeys({self.keys})"


@dataclass
class EventConfig:
    mouse_position: tuple[int, int]
    mouse_pressed: tuple[bool, bool, bool]
    mouse_wheel_state: MouseWheelState
    ctrl_alt_shift_array: tuple[bool, bool, bool]

    keys_pressed: ScancodeWrapper
    keys_just_pressed: SimulatedScancodeWrapper
    keys_just_released: SimulatedScancodeWrapper
