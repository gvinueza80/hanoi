import pygame
from config import *

class UI:
    """Handles all rendering and HUD display."""

    def __init__(self, surface, font_size=24):
        self.surface = surface
        self.font = pygame.font.Font(None, font_size)
        self.large_font = pygame.font.Font(None, int(font_size * 1.5))

    def draw_board(self):
        """Draw the game board background."""
        self.surface.fill(COLOR_BLACK)

        # Draw grid (optional, for debugging)
        # for x in range(0, self.surface.get_width(), GRID_SIZE):
        #     pygame.draw.line(self.surface, COLOR_DARK_GRAY, (x, 0), (x, self.surface.get_height()))
        # for y in range(0, self.surface.get_height(), GRID_SIZE):
        #     pygame.draw.line(self.surface, COLOR_DARK_GRAY, (0, y), (self.surface.get_width(), y))

    def draw_game_state(self, game_state):
        """Draw all game entities based on mode."""
        self.draw_board()

        # Draw obstacles
        for obstacle in game_state.get('obstacles', []):
            obstacle.draw(self.surface)

        # Draw food
        for food in game_state.get('foods', []):
            food.draw(self.surface)

        # Draw power-ups
        for powerup in game_state.get('powerups', []):
            powerup.draw(self.surface)

        # Draw snakes
        for snake in game_state.get('snakes', []):
            snake.draw(self.surface)

        # Draw HUD based on mode
        mode = game_state.get('mode')
        if mode == MODE_ARCADE:
            self.draw_arcade_hud(game_state)
        elif mode == MODE_TIME_ATTACK:
            self.draw_time_attack_hud(game_state)
        elif mode == MODE_PUZZLE:
            self.draw_puzzle_hud(game_state)

    def draw_arcade_hud(self, game_state):
        """Draw HUD for arcade mode."""
        scores = game_state.get('scores', [0])
        difficulty = game_state.get('difficulty', 0)

        # Player 1 score
        score_text = self.font.render(f"P1 Score: {scores[0]}", True, COLOR_WHITE)
        self.surface.blit(score_text, (10, 10))

        # Player 2 score (if multiplayer)
        if len(scores) > 1:
            score_text = self.font.render(f"P2 Score: {scores[1]}", True, COLOR_BLUE)
            self.surface.blit(score_text, (self.surface.get_width() - 250, 10))

        # Difficulty
        diff_text = self.font.render(f"Difficulty: {int(difficulty)}", True, COLOR_YELLOW)
        self.surface.blit(diff_text, (10, 40))

    def draw_time_attack_hud(self, game_state):
        """Draw HUD for time attack mode."""
        score = game_state.get('score', 0)
        time_remaining = game_state.get('time_remaining', 0)

        score_text = self.font.render(f"Score: {score}", True, COLOR_WHITE)
        self.surface.blit(score_text, (10, 10))

        time_text = self.font.render(f"Time: {time_remaining:.1f}s", True, COLOR_YELLOW)
        self.surface.blit(time_text, (self.surface.get_width() - 200, 10))

    def draw_puzzle_hud(self, game_state):
        """Draw HUD for puzzle mode."""
        level = game_state.get('level', 1)
        score = game_state.get('score', 0)

        level_text = self.font.render(f"Level: {level}", True, COLOR_WHITE)
        self.surface.blit(level_text, (10, 10))

        score_text = self.font.render(f"Score: {score}", True, COLOR_YELLOW)
        self.surface.blit(score_text, (10, 40))

    def draw_menu(self, selected_option=0):
        """Draw main menu."""
        self.surface.fill(COLOR_BLACK)

        title = self.large_font.render("SNAKE GAME", True, COLOR_RED)
        self.surface.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, 50))

        options = ["Arcade (Single)", "Arcade (Multiplayer)", "Time Attack", "Puzzle"]
        for i, option in enumerate(options):
            color = COLOR_YELLOW if i == selected_option else COLOR_WHITE
            text = self.font.render(option, True, color)
            self.surface.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2, 150 + i * 60))

    def draw_game_over(self, game_state):
        """Draw game over screen."""
        self.draw_game_state(game_state)

        # Semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(COLOR_BLACK)
        self.surface.blit(overlay, (0, 0))

        # Game over text
        game_over_text = self.large_font.render("GAME OVER", True, COLOR_RED)
        self.surface.blit(game_over_text, (WINDOW_WIDTH // 2 - game_over_text.get_width() // 2, 200))

        # Score
        mode = game_state.get('mode')
        if mode == MODE_ARCADE:
            scores = game_state.get('scores', [0])
            score_text = self.font.render(f"Final Score: {scores[0]}", True, COLOR_WHITE)
        else:
            score = game_state.get('score', 0)
            score_text = self.font.render(f"Final Score: {score}", True, COLOR_WHITE)

        self.surface.blit(score_text, (WINDOW_WIDTH // 2 - score_text.get_width() // 2, 300))

        # Instructions
        instructions = self.font.render("Press SPACE to return to menu", True, COLOR_YELLOW)
        self.surface.blit(instructions, (WINDOW_WIDTH // 2 - instructions.get_width() // 2, 400))
