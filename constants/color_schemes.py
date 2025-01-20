from constants.enums import QuadButtonState

BUTTON_COLOR_DICT1 = {
    QuadButtonState.NORMAL: (235, 165, 5),
    QuadButtonState.HOVER: (235, 190, 0),
    QuadButtonState.PRESSED: (180, 155, 5),
    QuadButtonState.PRESSED_OUTSIDE: (255, 255, 255),
}
BUTTON_COLOR_DICT2 = {
    QuadButtonState.NORMAL: (211, 245, 245),
    QuadButtonState.HOVER: (224, 245, 245),
    QuadButtonState.PRESSED: (228, 214, 255),
    QuadButtonState.PRESSED_OUTSIDE: (214, 255, 228),
}

buttons_color_schemes_dict: dict[str | int | None, dict] = {
    None: BUTTON_COLOR_DICT2,
    1: BUTTON_COLOR_DICT1
}
