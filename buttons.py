import pygame
from button_states import ButtonState
from abc import ABC
from commands import Command
import json
import os
from constants import *


class Button(ABC):
    def __init__(self, text, command: Command, position, size, colors, font=None, radius=10, fixed=True):
        self.position = position
        self.fixed = fixed
        self.dragging = False
        self.dragging_start_mouse = None
        self.dragging_start_top_left = None

        self.text = text
        self.size = size
        self.rect = pygame.Rect(position, size)

        self.command = command

        if font is None:
            font = pygame.font.SysFont('Tahoma', 30)
        self.font = font

        self.current_state = ButtonState.NORMAL

        self.radius = radius
        self.colors = colors  # Словарь с ключами: ButtonState.NORMAL, ButtonState.HOVER, ButtonState.ACTIVE
        self.sprites = {
            ButtonState.NORMAL: self.create_sprite(colors[ButtonState.NORMAL]),
            ButtonState.HOVER: self.create_sprite(colors[ButtonState.HOVER]),
            ButtonState.ACTIVE: self.create_sprite(colors[ButtonState.ACTIVE])
        }

    def create_sprite(self, color):
        sprite = pygame.Surface(self.size, pygame.SRCALPHA)
        pygame.draw.rect(sprite, color, sprite.get_rect(), border_radius=self.radius)
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=sprite.get_rect().center)
        sprite.blit(text_surface, text_rect)
        return sprite

    def draw(self, screen):
        screen.blit(self.sprites[self.current_state], self.rect)

    def handle_event(self, mouse_position, mouse_pressed, can_be_dragged=True) -> None | Command:
        unpressed = False
        if self.rect.collidepoint(mouse_position):
            if mouse_pressed[0]:  # LMB
                self.current_state = ButtonState.ACTIVE
            elif mouse_pressed[2] and can_be_dragged:  # RMB
                self.handle_dragging(mouse_position)
            else:
                if self.current_state == ButtonState.ACTIVE:
                    unpressed = True
                    print(f"Button '{self.text}' clicked (unpressed)")
                self.current_state = ButtonState.HOVER
                self.dragging = False
        else:
            self.current_state = ButtonState.NORMAL
            self.dragging = False

        if unpressed:
            return self.command

    def handle_dragging(self, mouse_position):
        if not self.dragging and not self.fixed:
            self.dragging = True
            self.dragging_start_mouse = mouse_position
            self.dragging_start_top_left = self.rect.topleft
        else:
            offset_x = mouse_position[0] - self.dragging_start_mouse[0]
            offset_y = mouse_position[1] - self.dragging_start_mouse[1]
            self.rect.x = self.dragging_start_top_left[0] + offset_x
            self.rect.y = self.dragging_start_top_left[1] + offset_y
            if not SCREEN_RECT.contains(self.rect.inflate(-10, -10)):
                self.rect.topleft = self.dragging_start_top_left


def load_button_positions(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    return []


def save_button_positions(buttons, file_path):
    positions = [{'text': button.text, 'position': button.rect.topleft} for button in buttons]
    with open(file_path, 'w') as file:
        json.dump(positions, file)
