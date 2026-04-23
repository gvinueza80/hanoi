import pygame
import json
import os
from config import *
from modes import ArcadeMode, TimeAttackMode, PuzzleMode
from ui import UI


class InputHandler:
    """Handles keyboard input."""

    def __init__(self):
        self.pressed_keys = set()

    def handle_events(self):
        """Process events and return quit signal."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            elif event.type == pygame.KEYDOWN:
                self.pressed_keys.add(event.key)
            elif event.type == pygame.KEYUP:
                self.pressed_keys.discard(event.key)
        return False

    def is_key_pressed(self, key):
        """Check if a key is currently pressed."""
        return key in self.pressed_keys


class Game:
    """Main game class managing game loop and mode switching."""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.running = True
        self.input_handler = InputHandler()
        self.ui = UI(self.screen)

        self.state = "menu"
        self.current_mode = None
        self.selected_menu_option = 0
        self.paused = False
        self.leaderboard = self.load_leaderboard()

    def load_leaderboard(self):
        """Load high scores from file."""
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r') as f:
                    return json.load(f)
            except:
                pass

        return {
            MODE_ARCADE: [],
            MODE_TIME_ATTACK: [],
            MODE_PUZZLE: []
        }

    def save_leaderboard(self):
        """Save high scores to file."""
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        with open(DATA_FILE, 'w') as f:
            json.dump(self.leaderboard, f, indent=2)

    def handle_menu_input(self):
        """Handle input in menu state."""
        if self.input_handler.is_key_pressed(pygame.K_UP):
            self.selected_menu_option = (self.selected_menu_option - 1) % 4
            pygame.time.wait(100)
        elif self.input_handler.is_key_pressed(pygame.K_DOWN):
            self.selected_menu_option = (self.selected_menu_option + 1) % 4
            pygame.time.wait(100)
        elif self.input_handler.is_key_pressed(pygame.K_RETURN):
            self.start_game(self.selected_menu_option)

    def start_game(self, option):
        """Start a new game based on menu selection."""
        if option == 0:  # Arcade Single
            self.current_mode = ArcadeMode(WINDOW_WIDTH, WINDOW_HEIGHT, multiplayer=False)
        elif option == 1:  # Arcade Multiplayer
            self.current_mode = ArcadeMode(WINDOW_WIDTH, WINDOW_HEIGHT, multiplayer=True)
        elif option == 2:  # Time Attack
            self.current_mode = TimeAttackMode(WINDOW_WIDTH, WINDOW_HEIGHT)
        elif option == 3:  # Puzzle
            self.current_mode = PuzzleMode(WINDOW_WIDTH, WINDOW_HEIGHT)

        self.state = "playing"
        self.paused = False

    def handle_game_input(self):
        """Handle input during gameplay."""
        if self.input_handler.is_key_pressed(pygame.K_p):
            self.paused = not self.paused
            pygame.time.wait(200)
        elif self.input_handler.is_key_pressed(pygame.K_ESCAPE):
            self.state = "menu"

    def update(self, dt):
        """Update game state."""
        if self.state == "menu":
            self.handle_menu_input()
        elif self.state == "playing":
            self.handle_game_input()

            if not self.paused:
                self.current_mode.update(dt, self.input_handler)

                if self.current_mode.is_over():
                    self.state = "game_over"

    def render(self):
        """Render game state."""
        if self.state == "menu":
            self.ui.draw_menu(self.selected_menu_option)
        elif self.state == "playing":
            game_state = self.current_mode.get_state()
            self.ui.draw_game_state(game_state)

            if self.paused:
                pause_text = self.ui.font.render("PAUSED", True, COLOR_YELLOW)
                self.screen.blit(pause_text, (WINDOW_WIDTH // 2 - pause_text.get_width() // 2, 300))
        elif self.state == "game_over":
            game_state = self.current_mode.get_state()
            self.ui.draw_game_over(game_state)

            if self.input_handler.is_key_pressed(pygame.K_SPACE):
                self.state = "menu"
                pygame.time.wait(200)

        pygame.display.flip()

    def run(self):
        """Main game loop."""
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0  # Delta time in seconds

            if self.input_handler.handle_events():
                self.running = False
                break

            self.update(dt)
            self.render()

        pygame.quit()
