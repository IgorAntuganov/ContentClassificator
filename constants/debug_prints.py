from enum import Enum

class DebugStates(Enum):
    HANDLERS_REGISTERING = False
    FOCUS = False
    DRAGGING = False
    HOVER = False
    CURSOR = False

def debug_print(debug_state: DebugStates, *args):
    if debug_state.value:
        print(f"[debug print: {debug_state.name}]", *args)
