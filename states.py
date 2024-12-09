from enum import Enum

class TripleButtonState(Enum):
    NORMAL = 1
    HOVER = 2
    PRESSED = 3
    PRESSED_OUTSIDE = 4

class DraggingState(Enum):
    STARTING = 1
    KEEPING = 2
    ENDING = 3
    OFFED = 4

class MouseWheelState(Enum):
    UP = 1
    INACTIVE = 0
    DOWN = -1

class CtrlAltState(Enum):
    INACTIVE = 0
    CTRL = 1
    ALT = 2
    CTRL_ALT = 3
