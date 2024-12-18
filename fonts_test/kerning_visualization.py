import pygame
pygame.init()
import itertools
import random
import json
import os

FONT_PATH = 'kerned_AtoS.ttf'
PROGRESS_FILE = "kerning_progress.json"

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r') as f:
            return json.load(f)
    return {char: "" for char in chars}

def save_progress(progress):
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(progress, f, indent=2)


WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SRCALPHA)
pygame.display.set_caption("Kerning Pair Generator")

WHITE = (215, 215, 215)
BLACK = (35, 35, 35)
DIM = (174, 174, 174)

large_font = pygame.font.Font(FONT_PATH, 200)
small_font = pygame.font.Font(FONT_PATH, 36)
tiny_font = pygame.font.Font(FONT_PATH, 18)

chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 ~!?#@$%&\'\"^_`*+,-./:;<=>(){|}[\\]"

char_pairs = list(itertools.product(chars, repeat=2))
current_pair_index = 0
progress = load_progress()
total_pairs_per_char = len(chars)

def random_phrase(pair):
    phrase = ''.join(random.choice(chars) for _ in range(8))
    return phrase[:3] + ''.join(pair) + phrase[3:]


def get_color(char, progress, first_char):
    viewed = len(progress[char])
    total = len(chars)
    if char == first_char:
        progress_value = viewed / total
        return 0, int(255 * progress_value),  int(255 * (1 - progress_value))
    elif viewed == total:
        return 110, 200, 110
    elif viewed == 0:
        return 60, 60, 60
    else:
        progress_value = viewed / total
        return int(255 * (1 - progress_value)), 0, int(255 * progress_value)


running = True
current_pair = char_pairs[current_pair_index]
phrase = random_phrase(current_pair)
pair_changed = True
while running:
    keys = pygame.key.get_pressed()
    ctrl_pressed = keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]
    shift_pressed = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
    space_pressed = keys[pygame.K_SPACE]
    value = 1
    if ctrl_pressed:
        value *= 10
    if shift_pressed:
        value *= total_pairs_per_char

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                current_pair_index = current_pair_index - value
                pair_changed = True
            elif event.key == pygame.K_RIGHT:
                current_pair_index = current_pair_index + value
                pair_changed = True

            elif event.key == pygame.K_SPACE:
                with open("kerning_pairs.txt", "a") as f:
                    f.write(''.join(char_pairs[current_pair_index]) + "\n")

    if pair_changed:
        current_pair_index %= len(char_pairs)
        current_pair = char_pairs[current_pair_index]
        phrase = random_phrase(current_pair)
        first_char, second_char = char_pairs[current_pair_index]
        if second_char not in progress[first_char]:
            saved_chars = progress[first_char]
            saved_chars += second_char
            new_chars = ''
            for _chr in chars:
                if _chr in saved_chars:
                    new_chars += _chr
            progress[first_char] = new_chars
            save_progress(progress)

    pair_changed = False

    screen.fill(WHITE)

    first_char, second_char = current_pair
    first_char_label = tiny_font.render('first char:', True, DIM)
    screen.blit(first_char_label, (10, 10))
    second_char_label = tiny_font.render('second char:', True, DIM)
    screen.blit(second_char_label, (WIDTH//2, 10))

    for i, char in enumerate(chars):
        color = get_color(char, progress, first_char)
        char_text = tiny_font.render(char, True, color)
        x = 10 + (i % 20) * 18
        y = 35 + (i // 20) * 18
        screen.blit(char_text, (x, y))

    progress_string = progress[first_char]
    for i, char in enumerate(chars):
        if char == second_char:
            color = 110, 110, 200
        elif char in progress_string:
            color = 110, 200, 110
        else:
            color = 45, 45, 45
        char_text = tiny_font.render(char, True, color)
        x = WIDTH//2 + (i % 20) * 18
        y = 35 + (i // 20) * 18
        screen.blit(char_text, (x, y))

    current_index_text = tiny_font.render(f"{current_pair_index}/{len(char_pairs)}", True, DIM)
    rect = current_index_text.get_rect(center=(WIDTH//2, HEIGHT*11.5//16))
    screen.blit(current_index_text, rect)

    large_text = large_font.render(''.join(current_pair), True, BLACK, (123, 189, 123) if space_pressed else None)
    rect = large_text.get_rect(center=(WIDTH//2, HEIGHT//2))
    screen.blit(large_text, rect)

    small_text = small_font.render(phrase, True, BLACK)
    rect = small_text.get_rect(center=(WIDTH//2, HEIGHT*13.5//16))
    screen.blit(small_text, rect)

    pygame.display.flip()
