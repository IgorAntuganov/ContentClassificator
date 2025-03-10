from enum import Enum, auto


class QuadButtonState(Enum):
    NORMAL = auto()
    HOVER = auto()
    PRESSED = auto()
    PRESSED_OUTSIDE = auto()


class InputFieldState(Enum):
    ACTIVE = auto()
    INACTIVE = auto()
    HOVERED = auto()
    PRESSED = auto()


class DraggingState(Enum):
    STARTING = auto()
    KEEPING = auto()
    ENDING = auto()
    OFFED = auto()


class MouseWheelState(Enum):
    UP = 1
    INACTIVE = 0
    DOWN = -1


class TargetPriority(Enum):
    ZERO = 0
    HOVER = 1
    DRAGGING = 2
