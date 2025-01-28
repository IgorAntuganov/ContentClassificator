from abc import ABC, abstractmethod

from UI_elements.UI_abstracts import WithPrivateRect, JSONadjustable
from UI_elements.abstract_element import UIElement

from commands.abstract_commands import CommandList
from commands.dragging_commands import StartDragging, KeepDragging, EndDragging
from commands.cursor_commands import ClearCursor, DraggingCursor

from constants.constants import SCREEN_RECT, BUTTON_SCREEN_COLLISION_DEFLATION
from constants.enums import DraggingState
from constants.configs import EventConfig


class Draggable(WithPrivateRect, UIElement, ABC):
    def __init__(self, position: tuple[int, int], size: tuple[int, int]):
        self.position = position
        WithPrivateRect.__init__(self, position, size)
        self.dragging:                         DraggingState = DraggingState.OFFED
        self.dragging_start_mouse:    None | tuple[int, int] = None
        self.dragging_start_top_left: None | tuple[int, int] = None

    @property
    def is_dragging(self) -> bool:
        return self.dragging != DraggingState.OFFED

    def _update_dragging_state(self, config: EventConfig) -> CommandList:
        commands_lst: CommandList
        commands_lst = []
        mouse_on_element = self.rect_collidepoint(config.mouse_position)
        rmb_pressed = config.mouse_pressed[2]

        if self.dragging == DraggingState.OFFED:
            if mouse_on_element and rmb_pressed:
                self.dragging = DraggingState.STARTING
                self.dragging_start_mouse = config.mouse_position
                self.dragging_start_top_left = self.get_rect_topleft()
                commands_lst.append(DraggingCursor())
                commands_lst.append(StartDragging())

        elif self.dragging == DraggingState.STARTING:
            commands_lst.append(KeepDragging())
            if not rmb_pressed:
                self.dragging = DraggingState.KEEPING

        elif self.dragging == DraggingState.KEEPING:
            commands_lst.append(KeepDragging())
            if rmb_pressed:
                self.dragging = DraggingState.ENDING

        elif self.dragging == DraggingState.ENDING:
            if rmb_pressed:
                commands_lst.append(KeepDragging())
            else:
                commands_lst.append(EndDragging())
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
            self.set_top_left((x, y))
            rect = self.get_rect()
            if not SCREEN_RECT.contains(rect.inflate(*BUTTON_SCREEN_COLLISION_DEFLATION)):
                self.set_top_left(self.dragging_start_top_left)

        return commands_lst

class Resizable(Draggable, WithPrivateRect, UIElement, ABC):
    @abstractmethod
    def recreate_sprites_after_resizing(self):
        pass

    def handle_dragging(self, config: EventConfig) -> CommandList:
        self.handle_size_changing(config.ctrl_alt_shift_array, config.mouse_wheel_state)
        return super().handle_dragging(config)

    def handle_size_changing(self, ctrl_alt_shift_array, mouse_wheel_state):
        sign = mouse_wheel_state.value
        if ctrl_alt_shift_array[2]:
            value = sign
        else:
            value = sign * 5

        curr_size = self.get_size()
        new_width, new_height = curr_size
        if ctrl_alt_shift_array[0]:
            new_width += value
        if ctrl_alt_shift_array[1]:
            new_height += value

        self.set_size((new_width, new_height))
        self.recreate_sprites_after_resizing()


class OnlyDraggableElement(JSONadjustable, Draggable, ABC):
    def __init__(self, path_to_json: str,
                 position: tuple[int, int],
                 size: tuple[int, int],
                 **kwargs):
        JSONadjustable.__init__(self, path_to_json, position=position, size=size, **kwargs)
        Draggable.__init__(self, self.position, self.size)


class DraggableAndResizableElement(Resizable, OnlyDraggableElement, ABC):
    pass
