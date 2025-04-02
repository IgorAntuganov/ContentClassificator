from dataclasses import dataclass
from UI_elements.abstract_element import UIElement
from constants.enums import TargetPriority
from UI_elements.manual_adjusting import Draggable


@dataclass
class FocusState:
    elements_order: list[UIElement]
    current_target: UIElement | None = None
    priority: TargetPriority = TargetPriority.ZERO
    last_active_tick: int = -1


class FocusManager:
    def __init__(self, elements_dct: dict[str, UIElement]):
        self._elements = elements_dct
        self._state = FocusState(list(elements_dct.values()))
        self._current_tick = 0

    def add_new_element(self, element_name: str, element: UIElement):
        assert element not in self._elements.values()
        self._elements[element_name] = element
        self._state.elements_order.append(element)

    def tick(self) -> None:
        self._current_tick += 1

    def get_target(self) -> None | UIElement | Draggable:
        return self._state.current_target

    def get_targeted_element(self) -> UIElement | Draggable:
        assert self._state.current_target is not None
        return self._state.current_target

    def claim_focus(self, element: UIElement, priority: TargetPriority):
        self._validate_element(element)
        assert self._state.current_target is None or priority.value > self._state.priority.value
        self._set_new_target(element, priority)

    def renew_focus(self, element: UIElement, priority: TargetPriority):
        self._validate_focus(element, priority)
        self._state.last_active_tick = self._current_tick

    def release_focus(self, element: UIElement, level: TargetPriority):
        self._validate_focus(element, level)
        self._reset_focus()

    @property
    def is_dragging(self) -> bool:
        return self._state.priority == TargetPriority.DRAGGING

    @property
    def is_hovering(self) -> bool:
        return self._state.priority == TargetPriority.HOVER

    def _validate_element(self, element: UIElement):
        assert element in self._elements.values()
        assert self._state.current_target is None

    def _validate_focus(self, element: UIElement, priority: TargetPriority):
        assert self._state.current_target is element
        assert self._state.priority == priority

    def _set_new_target(self, element: UIElement, priority: TargetPriority):
        self._state.current_target = element
        self._state.priority = priority
        self._state.last_active_tick = self._current_tick

    def _reset_focus(self):
        self._state.current_target = None
        self._state.priority = TargetPriority.ZERO
        self._state.last_active_tick = -1
