from constants.enums import QuadButtonState
from constants.enums import InputFieldState


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


INPUT_FIELD_COLOR_DICT = {
    InputFieldState.INACTIVE: (255, 206, 246),
    InputFieldState.HOVERED: (255, 217, 248),
    InputFieldState.PRESSED: (255, 178, 242),
    InputFieldState.ACTIVE: (204, 255, 247),
}

input_fields_colors: dict[str | int | None, dict] = {
    None: INPUT_FIELD_COLOR_DICT
}
