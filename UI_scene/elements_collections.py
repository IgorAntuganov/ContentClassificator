from dataclasses import dataclass
from UI_elements.abstract_element import AbstractUIElement
from constants.states import TargetPriority
from UI_elements.manual_adjusting import Draggable


@dataclass
class SceneElements:
    elements_lst: list[AbstractUIElement]
    elements_set: set[AbstractUIElement]
    interaction_target: None | AbstractUIElement | Draggable = None
    interaction_target_level: TargetPriority = TargetPriority.ZERO


class SceneElementsManager:
    def __init__(self, elements: SceneElements):
        self.elements = elements

    def get_targeted_element(self) -> None | AbstractUIElement | Draggable:
        return self.elements.interaction_target


    def set_interation_element(self, element: AbstractUIElement, level: TargetPriority):
        assert self.check_if_element_can_be_targeted(element, level)
        self.elements.interaction_target = element
        self.elements.interaction_target_level = level
        self.elements.elements_lst.remove(element)
        self.elements.elements_lst.append(element)

    def clear_interation_element(self, element: AbstractUIElement, level: TargetPriority):
        assert self.is_element_targeted(element, level)
        self.elements.interaction_target = None
        self.elements.interaction_target_level = TargetPriority.ZERO


    def check_if_element_can_be_targeted(self, element: AbstractUIElement, level: TargetPriority) -> bool:
        is_not_none = self.elements.interaction_target is None
        level_higher = self.elements.interaction_target_level.value < level.value
        in_scene = element in self.elements.elements_set
        return (is_not_none or level_higher) and in_scene

    def is_element_targeted(self, element: AbstractUIElement, level: TargetPriority) -> bool:
        is_same = self.elements.interaction_target is element
        exact_level = self.elements.interaction_target_level.value == level.value
        return is_same or exact_level


    @property
    def is_dragging(self) -> bool:
        return self.elements.interaction_target_level == TargetPriority.DRAGGING

    @property
    def is_hovering(self) -> bool:
        return self.elements.interaction_target_level == TargetPriority.HOVER


    def get_ordered_elements(self) -> list[AbstractUIElement]:
        return self.elements.elements_lst

    def get_elements_for_interaction(self) -> list[AbstractUIElement]:
        if self.elements.interaction_target_level != TargetPriority.ZERO:
            return [self.elements.interaction_target]
        return self.elements.elements_lst
