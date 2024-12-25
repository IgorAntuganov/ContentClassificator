FOCUS_DEBUG_PRINTING = False
DRAGGING_DEBUG_PRINTING = False
HOVER_DEBUG_PRINTING = False
HANDLERS_REGISTERING_PRINTING = False

if FOCUS_DEBUG_PRINTING:
    def debug_print(*args): print(*args)
else:
    def debug_print(*args): len(args)

if DRAGGING_DEBUG_PRINTING:
    def dragging_debug_print(*args): print(*args)
else:
    def dragging_debug_print(*args):
        len(args)

if HOVER_DEBUG_PRINTING:
    def hover_debug_print(*args): print(*args)
else:
    def hover_debug_print(*args):
        len(args)

if HANDLERS_REGISTERING_PRINTING:
    def handlers_registering_print(*args): print(*args)
else:
    def handlers_registering_print(*args):
        len(args)
