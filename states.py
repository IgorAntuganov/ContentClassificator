from enum import Enum, auto

class QuadButtonState(Enum):
    NORMAL = auto()
    HOVER = auto()
    PRESSED = auto()
    PRESSED_OUTSIDE = auto()

class DraggingState(Enum):
    STARTING = auto()
    KEEPING = auto()
    ENDING = auto()
    OFFED = auto()

class MouseWheelState(Enum):
    UP = 1
    INACTIVE = 0
    DOWN = -1

class CtrlAltState(Enum):
    INACTIVE = auto()
    CTRL = auto()
    ALT = auto()
    CTRL_ALT = auto()
