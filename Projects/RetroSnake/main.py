import sys
import pygame
import random
import os
import math
import json
import logging

# Logging
logging.basicConfig(level=logging.DEBUG, filename="debug.log", filemode="w",
                    format="%(asctime)s - %(levelname)s - %(message)s")

# Init
pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)  # Fix for some audio issues

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 400
BLOCK_SIZE = 10
WHITE = (255, 255, 255)
GREEN = (0, 255, 100)
DARK_GREEN = (0, 200, 80)
RED = (255, 50, 50)
BLUE = (50, 150, 255)
YELLOW = (255, 200, 0)
FPS_BASE = 10
ASSETS = "assets"
LEADERBOARD_FILE = "leaderboard.json"

# Screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Retro Snake")
clock = pygame.time.Clock()

# Fonts
font = pygame.font.SysFont("consolas", 20)
big_font = pygame.font.SysFont("consolas", 36)

# Load Sound
def load_sound(filename):
    try:
        path = os.path.join(ASSETS, filename)
        if os.path.exists(path):
            logging.info(f"Loading sound: {path}")
            return pygame.mixer.Sound(path)
        else:
            logging.warning(f"Sound not found: {path}")
    except Exception as e:
        logging.warning(f"Error loading {filename}: {e}")
    return None

eat_sound = load_sound("eat.wav")
game_over_sound = load_sound("game_over.wav")
menu_click = load_sound("menu_click.wav")
powerup_sound = load_sound("powerup.wav")
sound_enabled = True

# High score
HIGH_SCORE_FILE = "highscore.txt"
if os.path.exists(HIGH_SCORE_FILE):
    with open(HIGH_SCORE_FILE, "r") as f:
        try:
            high_score = int(f.read())
        except:
            high_score = 0
else:
    high_score = 0

def save_high_score(score):
    global high_score
    if score > high_score:
        high_score = score
        with open(HIGH_SCORE_FILE, "w") as f:
            f.write(str(high_score))

# Leaderboard
def load_leaderboard():
    if os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, "r") as f:
            return json.load(f)
    return []

def save_leaderboard(name, score):
    leaderboard = load_leaderboard()
    leaderboard.append({"name": name, "score": score})
    leaderboard = sorted(leaderboard, key=lambda x: x["score"], reverse=True)[:5]
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(leaderboard, f, indent=2)

# UI
def draw_text(text, size, color, x, y, center=True):
    f = pygame.font.SysFont("consolas", size)
    s = f.render(text, True, color)
    r = s.get_rect()
    if center:
        r.center = (x, y)
    else:
        r.topleft = (x, y)
    screen.blit(s, r)

def draw_background():
    for i in range(SCREEN_HEIGHT):
        color = (30 + int(25 * math.sin(i * 0.03)), 30, 30 + i % 40)
        pygame.draw.line(screen, color, (0, i), (SCREEN_WIDTH, i))

# Pause Menu
def pause_menu():
    paused = True
    selected = 0
    options = ["Resume", "Restart", "Quit"]
    while paused:
        screen.fill((0, 0, 0))
        draw_text("PAUSED", 36, YELLOW, SCREEN_WIDTH // 2, 60)
        for i, opt in enumerate(options):
            color = GREEN if i == selected else WHITE
            draw_text(opt, 24, color, SCREEN_WIDTH // 2, 140 + i * 40)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP, pygame.K_w]: selected = (selected - 1) % len(options)
                elif event.key in [pygame.K_DOWN, pygame.K_s]: selected = (selected + 1) % len(options)
                elif event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                    if selected == 0: return "resume"
                    elif selected == 1: return "restart"
                    elif selected == 2: pygame.quit(); sys.exit()

# Game Over
def game_over_screen(score):
    if sound_enabled and game_over_sound: game_over_sound.play()
    save_high_score(score)
    name = ""
    entering = True
    while entering:
        draw_background()
        draw_text("GAME OVER", 40, RED, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60)
        draw_text(f"Score: {score}", 24, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20)
        draw_text("Enter Name: " + name, 24, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10)
        draw_text("Press ENTER to save", 18, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name.strip():
                    save_leaderboard(name.strip(), score)
                    return
                elif event.key == pygame.K_BACKSPACE: name = name[:-1]
                elif len(name) < 12 and event.unicode.isprintable(): name += event.unicode

# Leaderboard
def leaderboard():
    viewing = True
    board = load_leaderboard()
    while viewing:
        screen.fill((0, 0, 0))
        draw_text("Top 5 Leaderboard", 32, YELLOW, SCREEN_WIDTH // 2, 40)
        for i, entry in enumerate(board):
            draw_text(f"{i+1}. {entry['name']} - {entry['score']}", 22, WHITE, SCREEN_WIDTH // 2, 100 + i * 30)
        draw_text("Press ESC to go back", 20, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: viewing = False

# Main Menu
def main_menu():
    global sound_enabled
    selected = 0
    options = ["Start Game", "Toggle Sound FX", "View Leaderboard", "Quit"]
    while True:
        screen.fill((0, 0, 0))
        draw_text("Retro Snake", 48, YELLOW, SCREEN_WIDTH // 2, 60)
        for i, option in enumerate(options):
            color = GREEN if i == selected else WHITE
            suffix = f": {'ON' if sound_enabled else 'OFF'}" if "Sound" in option else ""
            draw_text(option + suffix, 24, color, SCREEN_WIDTH // 2, 150 + i * 40)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP, pygame.K_w]: selected = (selected - 1) % len(options)
                elif event.key in [pygame.K_DOWN, pygame.K_s]: selected = (selected + 1) % len(options)
                elif event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                    if sound_enabled and menu_click: menu_click.play()
                    if selected == 0: return
                    elif selected == 1: sound_enabled = not sound_enabled
                    elif selected == 2: leaderboard()
                    elif selected == 3: pygame.quit(); sys.exit()

# Game
def play_game():
    snake_pos = [100, 50]
    snake_body = [[100, 50], [90, 50], [80, 50]]
    snake_dir = 'RIGHT'
    change_to = snake_dir
    food = [random.randrange(1, SCREEN_WIDTH // BLOCK_SIZE) * BLOCK_SIZE,
            random.randrange(1, SCREEN_HEIGHT // BLOCK_SIZE) * BLOCK_SIZE]
    power = None
    power_timer = 0
    score = 0
    speed = FPS_BASE

    while True:
        screen.fill((0, 0, 0))
        draw_background()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: save_high_score(score); pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    action = pause_menu()
                    if action == "resume": continue
                    elif action == "restart": return
                elif event.key in [pygame.K_UP, pygame.K_w] and snake_dir != 'DOWN': change_to = 'UP'
                elif event.key in [pygame.K_DOWN, pygame.K_s] and snake_dir != 'UP': change_to = 'DOWN'
                elif event.key in [pygame.K_LEFT, pygame.K_a] and snake_dir != 'RIGHT': change_to = 'LEFT'
                elif event.key in [pygame.K_RIGHT, pygame.K_d] and snake_dir != 'LEFT': change_to = 'RIGHT'

        snake_dir = change_to
        if snake_dir == 'UP': snake_pos[1] -= BLOCK_SIZE
        elif snake_dir == 'DOWN': snake_pos[1] += BLOCK_SIZE
        elif snake_dir == 'LEFT': snake_pos[0] -= BLOCK_SIZE
        elif snake_dir == 'RIGHT': snake_pos[0] += BLOCK_SIZE

        snake_pos[0] %= SCREEN_WIDTH
        snake_pos[1] %= SCREEN_HEIGHT
        snake_body.insert(0, list(snake_pos))

        if snake_pos == food:
            if sound_enabled and eat_sound: eat_sound.play()
            score += 10
            speed += 0.2
            food = [random.randrange(1, SCREEN_WIDTH // BLOCK_SIZE) * BLOCK_SIZE,
                    random.randrange(1, SCREEN_HEIGHT // BLOCK_SIZE) * BLOCK_SIZE]
            if random.randint(0, 4) == 2:
                power = [random.randrange(1, SCREEN_WIDTH // BLOCK_SIZE) * BLOCK_SIZE,
                         random.randrange(1, SCREEN_HEIGHT // BLOCK_SIZE) * BLOCK_SIZE]
                power_timer = 150
        else:
            snake_body.pop()

        if power:
            power_timer -= 1
            if snake_pos == power:
                if sound_enabled and powerup_sound: powerup_sound.play()
                score += 25
                power = None
            elif power_timer <= 0:
                power = None

        if snake_pos in snake_body[1:]: return game_over_screen(score)

        for i, block in enumerate(snake_body):
            color = GREEN if i == 0 else DARK_GREEN
            pygame.draw.rect(screen, color, pygame.Rect(block[0], block[1], BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(screen, RED, pygame.Rect(food[0], food[1], BLOCK_SIZE, BLOCK_SIZE))
        if power:
            pygame.draw.circle(screen, BLUE, (power[0] + 5, power[1] + 5), 6)

        # FIXED SCORE DISPLAY POSITION
        draw_text(f"Score: {score}  High: {high_score}", 20, WHITE, 10, 10, center=False)

        pygame.display.flip()
        clock.tick(speed)

# Run
try:
    while True:
        main_menu()
        play_game()
except Exception as e:
    logging.critical(f"Crash: {e}")
    pygame.quit()
    sys.exit()