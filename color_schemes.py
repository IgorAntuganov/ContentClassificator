from states import ButtonState

BUTTON_COLOR_DICT1 = {
    ButtonState.NORMAL: (235, 165, 5),
    ButtonState.HOVER: (235, 190, 0),
    ButtonState.ACTIVE: (180, 155, 5)
}
BUTTON_COLOR_DICT2 = {
    ButtonState.NORMAL: (224, 245, 245),
    ButtonState.HOVER: (255, 228, 225),
    ButtonState.ACTIVE: (216, 191, 216)
}

buttons_color_schemes_dict: dict[str | None: dict] = {
    None: BUTTON_COLOR_DICT2
}
