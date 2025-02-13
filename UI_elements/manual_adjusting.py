from abc import ABC

from UI_elements.abstract_element import UIElement

from commands.abstract_commands import CommandList
from commands.element_interaction_commands import StartDrag, ContinueDrag, StopDrag, ClearCursor, DraggingCursor

from constants.constants import SCREEN_RECT, BUTTON_SCREEN_COLLISION_DEFLATION
from constants.enums import DraggingState
from constants.configs import EventConfig


class Draggable(UIElement, ABC):
    def __init__(self):
        super().__init__()
        self.dragging:                         DraggingState = DraggingState.OFFED
        self.dragging_start_mouse:    None | tuple[int, int] = None
        self.dragging_start_top_left: None | tuple[int, int] = None

    @property
    def is_dragging(self) -> bool:
        return self.dragging != DraggingState.OFFED

    def _update_dragging_state(self, config: EventConfig) -> CommandList:
        commands_lst: CommandList
        commands_lst = []
        mouse_on_element = self.get_rect().collidepoint(config.mouse_position)
        rmb_pressed = config.mouse_pressed[2]

        if self.dragging == DraggingState.OFFED:
            if mouse_on_element and rmb_pressed:
                self.dragging = DraggingState.STARTING
                self.dragging_start_mouse = config.mouse_position
                self.dragging_start_top_left = self._savable_config.position
                commands_lst.append(DraggingCursor())
                commands_lst.append(StartDrag())

        elif self.dragging == DraggingState.STARTING:
            commands_lst.append(ContinueDrag())
            if not rmb_pressed:
                self.dragging = DraggingState.KEEPING

        elif self.dragging == DraggingState.KEEPING:
            commands_lst.append(ContinueDrag())
            if rmb_pressed:
                self.dragging = DraggingState.ENDING

        elif self.dragging == DraggingState.ENDING:
            if rmb_pressed:
                commands_lst.append(ContinueDrag())
            else:
                commands_lst.append(StopDrag())
                commands_lst.append(ClearCursor())
                self.dragging = DraggingState.OFFED

        return commands_lst

    def handle_dragging(self, config: EventConfig) -> CommandList:
        commands_lst = self._update_dragging_state(config)

        if self.dragging != DraggingState.OFFED:
            assert self.dragging_start_mouse is not None and self.dragging_start_top_left is not None
            offset_x = config.mouse_position[0] - self.dragging_start_mouse[0]
            offset_y = config.mouse_position[1] - self.dragging_start_mouse[1]
            x = self.dragging_start_top_left[0] + offset_x
            y = self.dragging_start_top_left[1] + offset_y
            self._savable_config.position = (x, y)
            rect = self.get_rect()
            if not SCREEN_RECT.contains(rect.inflate(*BUTTON_SCREEN_COLLISION_DEFLATION)):
                self._savable_config.position = self.dragging_start_top_left

        return commands_lst


class Resizable(Draggable, UIElement, ABC):
    def handle_dragging(self, config: EventConfig) -> CommandList:
        self.handle_size_changing(config.ctrl_alt_shift_array, config.mouse_wheel_state)
        return super().handle_dragging(config)

    def handle_size_changing(self, ctrl_alt_shift_array, mouse_wheel_state):
        sign = mouse_wheel_state.value
        if sign == 0:
            return

        if ctrl_alt_shift_array[2]:
            value = sign
        else:
            value = sign * 5

        curr_size = self._savable_config.size
        new_width, new_height = curr_size
        if ctrl_alt_shift_array[0]:
            new_width += value
        if ctrl_alt_shift_array[1]:
            new_height += value

        self._savable_config.size = (new_width, new_height)
        self._draw_sprites()


class DraggableAndResizableElement(Resizable, ABC):
    pass
