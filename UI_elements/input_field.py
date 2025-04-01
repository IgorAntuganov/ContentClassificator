from dataclasses import dataclass
import time
import pygame

from constants.configs import EventConfig
from UI_elements.manual_adjusting import Resizable
from commands.abstract_commands import CommandList, base_command_alias
from commands.element_interaction_commands import StopHover, StartHover, ContinueHover

from constants.styles import input_fields_colors, key_to_font
from constants.enums import InputFieldState
import constants.constants as cnst

SATURATION_MULTI = 6
LONG_PRESSING_TIME = .5
LONG_PRESSING_FREQ = .04
CURSOR_LINE_THICKNESS = 2

LINE_COLOR = (0, 0, 0)
TEXT_COLOR = (0, 0, 0)
PLACEHOLDER_ALPHA = 80


def saturate_color(r, g, b, saturation) -> tuple[int, int, int]:
    color_obj = pygame.Color(r, g, b)
    color_obj.hsva = (color_obj.hsva[0], min(100.0, color_obj.hsva[1] * saturation), color_obj.hsva[2], 100)
    return color_obj.r, color_obj.g, color_obj.b


@dataclass
class InputFieldConfig:
    placeholder_text: str
    max_length: int
    command: base_command_alias
    colors_key: str | int | None = None
    font_key: str | int | None = None


class LongPressTracking:
    def __init__(self):
        self._long_press_tracking: dict[int, list[float | None, int]] = {
            pygame.K_BACKSPACE: [None, 0],
            pygame.K_DELETE: [None, 0],
            pygame.K_LEFT: [None, 0],
            pygame.K_RIGHT: [None, 0],
        }

    def update_long_press_tracking(self, event_config: EventConfig):
        for key in self._long_press_tracking.keys():
            if not event_config.keys_pressed[key]:
                self._long_press_tracking[key] = [None, 0]
            elif self._long_press_tracking[key][0] is None:
                self._long_press_tracking[key] = [time.time(), 0]

    def check_long_pressing(self, key: int) -> bool:
        if self._long_press_tracking[key][0] is None:
            return False
        pressing_start = self._long_press_tracking[key][0]
        if time.time() - pressing_start < LONG_PRESSING_TIME:
            return False
        true_counter = self._long_press_tracking[key][1]
        expected_next_true_time = pressing_start + LONG_PRESSING_TIME + true_counter * LONG_PRESSING_FREQ
        if time.time() > expected_next_true_time:
            self._long_press_tracking[key][1] += 1
            return True
        return False


class InputField(Resizable):
    def __init__(self, config: InputFieldConfig):
        super().__init__()
        self.state = InputFieldState.INACTIVE
        self.hovered: bool = False
        self.command = config.command

        self._text: str = ''
        self._text_for_extraction: str | None = None
        self.cursor_position: int = 0
        self.placeholder_text = config.placeholder_text
        self.max_length = config.max_length
        self.tracker = LongPressTracking()

        self.font = key_to_font(config.font_key)
        assert config.colors_key in input_fields_colors
        self.colors = input_fields_colors[config.colors_key]

        self.sprite = pygame.Surface(self._savable_config.size, pygame.SRCALPHA)
        self._draw_sprites()

    def extract_text(self) -> str:
        assert self._text_for_extraction is not None
        text = self._text_for_extraction
        self._text_for_extraction = None
        return text

    def _left_padding(self):
        return self.font.get_height() // 2

    def _line_x(self, cursor_position):
        return self.font.size(self._text[:cursor_position])[0] + self._left_padding() - CURSOR_LINE_THICKNESS

    def _draw_sprites(self):
        multi = cnst.OUTLINE_DARKENING_COEFFICIENT
        color = self.colors[self.state]

        if self.state == InputFieldState.HOVERED:
            deflation = 0, 0
            text_descent = 0
            outline_color = list(map(lambda x: max(0, min(255, x * multi)), color))
        elif self.state == InputFieldState.INACTIVE:
            deflation = cnst.NORMAL_SPRITE_DEFLATION
            text_descent = cnst.NORMAL_TEXT_DESCENT
            outline_color = list(map(lambda x: max(0, min(255, x * multi)), color))
        else:
            deflation = cnst.ACTIVE_SPRITE_DEFLATION
            text_descent = cnst.ACTIVE_TEXT_DESCENT
            outline_color = saturate_color(*color, SATURATION_MULTI)

        self.sprite = pygame.Surface(self._savable_config.size, pygame.SRCALPHA)

        rect = self.sprite.get_rect().inflate(deflation)
        rect.move_ip(0, -deflation[1] // 2)
        smaller_rect = rect.inflate(cnst.BIG_OUTLINE_DEFLATION)

        pygame.draw.rect(self.sprite, outline_color, rect)
        pygame.draw.rect(self.sprite, color, smaller_rect)

        if len(self._text) > 0:
            text = self._text
            alpha = 255
        else:
            text = self.placeholder_text
            alpha = PLACEHOLDER_ALPHA

        left_offset = self._left_padding()
        text_surface = self.font.render(text, True, TEXT_COLOR)
        text_surface.set_alpha(alpha)
        text_rect = text_surface.get_rect(centery=self.sprite.get_rect().centery, left=left_offset)
        text_rect.move_ip(0, text_descent)
        self.sprite.blit(text_surface, text_rect)

        if self.state in (InputFieldState.PRESSED, InputFieldState.ACTIVE):
            line_x = self._line_x(self.cursor_position)
            start_pos = (line_x, text_rect.top)
            end_pos = (line_x, text_rect.bottom)
            pygame.draw.line(self.sprite, LINE_COLOR, start_pos, end_pos, CURSOR_LINE_THICKNESS)

    def get_sprite(self) -> pygame.Surface:
        return self.sprite

    def handle_events(self, event_config: EventConfig) -> CommandList:
        dragging_commands = self.handle_dragging(event_config)
        if len(dragging_commands) > 0:
            if self.hovered:
                dragging_commands.insert(0, StopHover())
                self.state = InputFieldState.INACTIVE
                self._draw_sprites()
            self.hovered = False
            return dragging_commands

        if self._is_inactive(event_config):
            return self._handle_inactive()
        return self._handle_active(event_config)

    def _is_inactive(self, mouse_config: EventConfig) -> bool:
        dragging_offed = not self.is_dragging
        not_pressed = self.state in (InputFieldState.INACTIVE, InputFieldState.HOVERED)
        not_collide = not self.get_rect().collidepoint(mouse_config.mouse_position)
        return dragging_offed and not_pressed and not_collide

    def _handle_inactive(self) -> CommandList:
        if self.state != InputFieldState.INACTIVE:
            self.state = InputFieldState.INACTIVE
            self._draw_sprites()
            self.hovered = False
            return [StopHover()]
        return []

    def _handle_active(self, event_config) -> CommandList:
        commands_lst: CommandList = []
        start_state, start_text, start_position = self.state.value, self._text, self.cursor_position

        self._update_state(commands_lst, event_config)
        commands_lst.extend(self._update_text_and_cursor(event_config))

        if (self._text != start_text) or (start_position != self.cursor_position) or (self.state.value != start_state):
            self._draw_sprites()
        return commands_lst

    def _update_state(self, commands_lst, event_config):
        if self.state == InputFieldState.INACTIVE:
            commands_lst.append(StartHover())
            self.state = InputFieldState.HOVERED
            self.hovered = True
        else:
            commands_lst.append(ContinueHover())

        if event_config.mouse_pressed[0]:  # LMB
            if self.get_rect().collidepoint(event_config.mouse_position):
                if self.state in (InputFieldState.INACTIVE, InputFieldState.HOVERED):
                    self.state = InputFieldState.PRESSED
            elif self.state == InputFieldState.ACTIVE:
                self.state = InputFieldState.INACTIVE
                commands_lst.append(StopHover())
                self.hovered = False
        elif self.state == InputFieldState.PRESSED:
            self.state = InputFieldState.ACTIVE

    def _end_input(self) -> CommandList:
        self._text_for_extraction = self._text
        self._text = ''
        self.hovered = False
        self.state = InputFieldState.INACTIVE
        return [StopHover(), self.command]

    def _update_text_and_cursor(self, event_config: EventConfig) -> CommandList:
        if self.state not in (InputFieldState.ACTIVE, InputFieldState.PRESSED):
            return []
        if paste := event_config.pasted_text:
            self._text = self._text[:self.cursor_position] + paste + self._text[self.cursor_position:]
            self.cursor_position += len(paste)
            return []
        self.tracker.update_long_press_tracking(event_config)
        keys = event_config.keys_just_pressed
        if keys[pygame.K_RETURN]:
            return self._end_input()
        if keys[pygame.K_BACKSPACE] or self.tracker.check_long_pressing(pygame.K_BACKSPACE):
            if self.cursor_position > 0:
                self._text = self._text[:self.cursor_position - 1] + self._text[self.cursor_position:]
                self.cursor_position -= 1
        elif keys[pygame.K_DELETE] or self.tracker.check_long_pressing(pygame.K_DELETE):
            if self.cursor_position < len(self._text):
                self._text = self._text[:self.cursor_position] + self._text[self.cursor_position + 1:]
        elif keys[pygame.K_LEFT] or self.tracker.check_long_pressing(pygame.K_LEFT):
            if self.cursor_position > 0:
                self.cursor_position -= 1
        elif keys[pygame.K_RIGHT] or self.tracker.check_long_pressing(pygame.K_RIGHT):
            if self.cursor_position < len(self._text):
                self.cursor_position += 1
        elif event_config.mouse_pressed[0]:
            self._update_cursor_with_mouse(event_config)
        else:
            for unicode in event_config.unicodes_just_pressed.keys:
                if len(self._text) < self.max_length and unicode:
                    self._text = self._text[:self.cursor_position] + unicode + self._text[self.cursor_position:]
                    self.cursor_position += 1
        return []

    def _update_cursor_with_mouse(self, event_config: EventConfig):
        mouse_x = event_config.mouse_position[0] - self.get_rect().left
        self.cursor_position = min(range(len(self._text) + 1), key=lambda i: abs(self._line_x(i) - mouse_x))
