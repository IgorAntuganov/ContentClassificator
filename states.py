from enum import Enum


class TripleButtonState(Enum):
    NORMAL = 1
    HOVER = 2
    ACTIVE = 3


class MouseWheelState(Enum):
    UP = 1
    INACTIVE = 0
    DOWN = -1


class CtrlAltState(Enum):
    INACTIVE = 0
    CTRL = 1
    ALT = 2
    CTRL_ALT = 3
