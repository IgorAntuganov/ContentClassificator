from states import TripleButtonState

BUTTON_COLOR_DICT1 = {
    TripleButtonState.NORMAL: (235, 165, 5),
    TripleButtonState.HOVER: (235, 190, 0),
    TripleButtonState.PRESSED: (180, 155, 5)
}
BUTTON_COLOR_DICT2 = {
    TripleButtonState.NORMAL: (224, 245, 245),
    TripleButtonState.HOVER: (255, 214, 209),  # (255, 228, 225)
    TripleButtonState.PRESSED: (228, 214, 255)  # (216, 191, 216)
}

buttons_color_schemes_dict: dict[str | int | None, dict] = {
    None: BUTTON_COLOR_DICT2,
    1: BUTTON_COLOR_DICT1
}
