from enum import Enum

class DebugStates(Enum):
    FOCUS = False
    DRAGGING = False
    HOVER = False
    HANDLERS_REGISTERING = False

def debug_print(debug_state: DebugStates, *args):
    if debug_state.value:
        print(f"[debug print: {debug_state.name}]", *args)
