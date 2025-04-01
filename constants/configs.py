from dataclasses import dataclass
from pygame.key import ScancodeWrapper
from constants.enums import MouseWheelState


class SimulatedScancodeWrapper:
    def __init__(self):
        self.keys: set[int | str] = set()

    def add(self, key: int | str):
        self.keys.add(key)

    def __contains__(self, key: int | str) -> bool:
        return key in self.keys

    def __getitem__(self, key: int | str) -> bool:
        return key in self.keys

    def __repr__(self) -> str:
        return f"SimulatedScancodeWrapper({self.keys})"


@dataclass
class EventConfig:
    mouse_position: tuple[int, int]
    mouse_pressed: tuple[bool, bool, bool]
    mouse_wheel_state: MouseWheelState
    ctrl_alt_shift_array: tuple[bool, bool, bool]

    keys_pressed: ScancodeWrapper
    keys_just_pressed: SimulatedScancodeWrapper
    keys_just_released: SimulatedScancodeWrapper

    unicodes_just_pressed: SimulatedScancodeWrapper
    unicodes_just_released: SimulatedScancodeWrapper

    pasted_text: str | None


from dataclasses import dataclass
from constants.constants import STANDARD_UI_SIZE, STANDARD_UI_POSITION


@dataclass
class SavableConfig:
    position: tuple[int, int] = STANDARD_UI_POSITION
    size: tuple[int, int] = STANDARD_UI_SIZE
