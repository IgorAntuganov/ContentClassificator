from states import TripleButtonState

BUTTON_COLOR_DICT1 = {
    TripleButtonState.NORMAL: (235, 165, 5),
    TripleButtonState.HOVER: (235, 190, 0),
    TripleButtonState.ACTIVE: (180, 155, 5)
}
BUTTON_COLOR_DICT2 = {
    TripleButtonState.NORMAL: (224, 245, 245),
    TripleButtonState.HOVER: (255, 228, 225),
    TripleButtonState.ACTIVE: (216, 191, 216)
}

buttons_color_schemes_dict: dict[str | None: dict] = {
    None: BUTTON_COLOR_DICT2
}
