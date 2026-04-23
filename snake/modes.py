import pygame
import random
from config import *
from entities import *
from collision import CollisionSystem

class GameMode:
    """Base class for all game modes."""

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid_width = width // GRID_SIZE
        self.grid_height = height // GRID_SIZE
        self.collision = CollisionSystem(self.grid_width, self.grid_height)
        self.reset()

    def reset(self):
        """Reset game state for this mode."""
        raise NotImplementedError

    def update(self, dt, input_handler):
        """Update game state."""
        raise NotImplementedError

    def get_state(self):
        """Return current game state (score, time, etc.)."""
        raise NotImplementedError

    def is_over(self):
        """Check if game is over."""
        raise NotImplementedError


class ArcadeMode(GameMode):
    """Endless arcade gameplay with progressive difficulty."""

    def __init__(self, width, height, multiplayer=False):
        self.multiplayer = multiplayer
        super().__init__(width, height)

    def reset(self):
        """Initialize arcade mode."""
        self.snakes = [
            Snake(self.grid_width // 4, self.grid_height // 2, COLOR_RED, is_player_1=True)
        ]
        if self.multiplayer:
            self.snakes.append(
                Snake(3 * self.grid_width // 4, self.grid_height // 2, COLOR_BLUE, is_player_1=False)
            )

        self.foods = []
        self.powerups = []
        self.obstacles = []
        self.scores = [0] * len(self.snakes)
        self.elapsed_time = 0.0
        self.difficulty = 0.0
        self.spawn_food()
        self.is_game_over = False

    def spawn_food(self):
        """Spawn a new food item."""
        is_bonus = random.random() < FOOD_BONUS_SPAWN_CHANCE
        x, y = self.collision.get_random_empty_cell(self.snakes, self.obstacles, self.foods, self.powerups)
        self.foods.append(Food(x, y, is_bonus))

    def spawn_powerup(self):
        """Spawn a random power-up."""
        powerup_types = [POWERUP_SPEED_BOOST, POWERUP_SHIELD, POWERUP_SCORE_MULTIPLIER, POWERUP_FREEZE]
        powerup_type = random.choice(powerup_types)
        x, y = self.collision.get_random_empty_cell(self.snakes, self.obstacles, self.foods, self.powerups)
        self.powerups.append(PowerUp(x, y, powerup_type))

    def spawn_obstacle(self):
        """Spawn a random obstacle based on current difficulty."""
        rand = random.random()
        if rand < STATIC_WALL_PROBABILITY:
            obstacle = StaticWall
        elif rand < STATIC_WALL_PROBABILITY + MOVING_WALL_PROBABILITY:
            obstacle = lambda: MovingWall(
                random.randint(1, self.grid_width - 2),
                random.randint(1, self.grid_height - 2)
            )
        elif rand < STATIC_WALL_PROBABILITY + MOVING_WALL_PROBABILITY + SPIKE_PROBABILITY:
            obstacle = Spike
        else:
            obstacle = Spiral

        if obstacle == Spike or obstacle == StaticWall:
            x, y = self.collision.get_random_empty_cell(self.snakes, self.obstacles, self.foods, self.powerups)
            self.obstacles.append(obstacle(x, y))
        else:
            x, y = self.collision.get_random_empty_cell(self.snakes, self.obstacles, self.foods, self.powerups)
            self.obstacles.append(obstacle())

    def update(self, dt, input_handler):
        """Update arcade mode."""
        if self.is_game_over:
            return

        self.elapsed_time += dt

        # Update difficulty every 7 seconds
        new_difficulty = int(self.elapsed_time / ARCADE_DIFFICULTY_INCREASE_INTERVAL)
        if new_difficulty > self.difficulty:
            self.difficulty = new_difficulty
            # Increase snake speed slightly
            for snake in self.snakes:
                snake.speed = min(SNAKE_MAX_SPEED, SNAKE_BASE_SPEED + self.difficulty * ARCADE_SPEED_INCREASE_PER_DIFFICULTY)

        # Update snakes based on input
        for i, snake in enumerate(self.snakes):
            if i == 0:  # Player 1
                if input_handler.is_key_pressed(pygame.K_UP):
                    snake.set_direction((0, -1))
                elif input_handler.is_key_pressed(pygame.K_DOWN):
                    snake.set_direction((0, 1))
                elif input_handler.is_key_pressed(pygame.K_LEFT):
                    snake.set_direction((-1, 0))
                elif input_handler.is_key_pressed(pygame.K_RIGHT):
                    snake.set_direction((1, 0))
            else:  # Player 2
                if input_handler.is_key_pressed(pygame.K_w):
                    snake.set_direction((0, -1))
                elif input_handler.is_key_pressed(pygame.K_s):
                    snake.set_direction((0, 1))
                elif input_handler.is_key_pressed(pygame.K_a):
                    snake.set_direction((-1, 0))
                elif input_handler.is_key_pressed(pygame.K_d):
                    snake.set_direction((1, 0))

            snake.update(dt)

        # Update obstacles
        for obstacle in self.obstacles:
            obstacle.update(dt)

        # Spawn obstacles based on difficulty
        if random.random() < min(OBSTACLE_SPAWN_RATE_MAX, OBSTACLE_SPAWN_RATE_INITIAL + self.difficulty * 0.02):
            self.spawn_obstacle()

        # Spawn powerups rarely
        if random.random() < 0.001:
            self.spawn_powerup()

        # Check collisions
        for i, snake in enumerate(self.snakes):
            # Wall collision
            if self.collision.snake_hits_wall(snake):
                snake.alive = False

            # Obstacle collision
            is_spike, obstacle = self.collision.snake_hits_obstacle(snake, self.obstacles)
            if is_spike:
                snake.alive = False
            elif obstacle and not snake.shield_active:
                snake.alive = False
            elif obstacle and snake.shield_active:
                snake.shield_active = False

            # Food collision
            food = self.collision.snake_eats_food(snake, self.foods)
            if food:
                snake.grow()
                self.scores[i] += int(food.points * snake.score_multiplier)
                self.foods.remove(food)
                if len(self.foods) == 0:
                    self.spawn_food()

            # Power-up collision
            powerup = self.collision.snake_gets_powerup(snake, self.powerups)
            if powerup:
                self.apply_powerup(snake, powerup)
                self.powerups.remove(powerup)

        # Check if snakes collide with each other
        if self.multiplayer and len(self.snakes) == 2:
            if self.collision.snakes_collide(self.snakes[0], self.snakes[1]):
                # Both die (or handle differently)
                pass

        # Check game over
        alive_count = sum(1 for snake in self.snakes if snake.alive)
        if alive_count == 0:
            self.is_game_over = True

    def apply_powerup(self, snake, powerup):
        """Apply power-up effect to snake."""
        if powerup.type == POWERUP_SPEED_BOOST:
            snake.speed = min(SNAKE_MAX_SPEED, snake.speed * POWERUP_SPEED_MULTIPLIER)
        elif powerup.type == POWERUP_SHIELD:
            snake.shield_active = True
        elif powerup.type == POWERUP_SCORE_MULTIPLIER:
            snake.score_multiplier = POWERUP_SCORE_MULTIPLIER
        # FREEZE handled globally in game loop

    def get_state(self):
        """Return current game state."""
        return {
            'mode': MODE_ARCADE,
            'snakes': self.snakes,
            'foods': self.foods,
            'powerups': self.powerups,
            'obstacles': self.obstacles,
            'scores': self.scores,
            'difficulty': self.difficulty,
            'game_over': self.is_game_over
        }

    def is_over(self):
        """Check if game is over."""
        return self.is_game_over


class TimeAttackMode(GameMode):
    """Survive within a time limit."""

    def __init__(self, width, height):
        super().__init__(width, height)

    def reset(self):
        """Initialize time attack mode."""
        self.snakes = [Snake(self.grid_width // 2, self.grid_height // 2, COLOR_RED)]
        self.foods = []
        self.powerups = []
        self.obstacles = []
        self.scores = [0]
        self.time_limit = TIME_ATTACK_INITIAL_TIME
        self.elapsed_time = 0.0
        self.difficulty = 0.0
        self.spawn_food()
        self.is_game_over = False

    def spawn_food(self):
        """Spawn food."""
        is_bonus = random.random() < FOOD_BONUS_SPAWN_CHANCE
        x, y = self.collision.get_random_empty_cell(self.snakes, self.obstacles, self.foods, self.powerups)
        self.foods.append(Food(x, y, is_bonus))

    def update(self, dt, input_handler):
        """Update time attack mode."""
        if self.is_game_over:
            return

        self.elapsed_time += dt

        # Check time limit
        if self.elapsed_time >= self.time_limit:
            self.is_game_over = True
            return

        # Update difficulty faster than arcade (every 10 seconds)
        new_difficulty = int(self.elapsed_time / TIME_ATTACK_DIFFICULTY_SPIKE_INTERVAL)
        if new_difficulty > self.difficulty:
            self.difficulty = new_difficulty
            # Increase snake speed slightly
            for snake in self.snakes:
                snake.speed = min(SNAKE_MAX_SPEED, SNAKE_BASE_SPEED + self.difficulty * ARCADE_SPEED_INCREASE_PER_DIFFICULTY)

        # Update snake based on input
        snake = self.snakes[0]
        if input_handler.is_key_pressed(pygame.K_UP):
            snake.set_direction((0, -1))
        elif input_handler.is_key_pressed(pygame.K_DOWN):
            snake.set_direction((0, 1))
        elif input_handler.is_key_pressed(pygame.K_LEFT):
            snake.set_direction((-1, 0))
        elif input_handler.is_key_pressed(pygame.K_RIGHT):
            snake.set_direction((1, 0))

        snake.update(dt)

        # Update obstacles
        for obstacle in self.obstacles:
            obstacle.update(dt)

        # Spawn obstacles aggressively (more than arcade)
        aggressive_spawn_rate = min(OBSTACLE_SPAWN_RATE_MAX, OBSTACLE_SPAWN_RATE_INITIAL + self.difficulty * 0.03)
        if random.random() < aggressive_spawn_rate:
            self.spawn_obstacle()

        # Spawn powerups rarely
        if random.random() < 0.001:
            self.spawn_powerup()

        # Check collisions
        # Wall collision
        if self.collision.snake_hits_wall(snake):
            snake.alive = False

        # Obstacle collision
        is_spike, obstacle = self.collision.snake_hits_obstacle(snake, self.obstacles)
        if is_spike:
            snake.alive = False
        elif obstacle and not snake.shield_active:
            snake.alive = False
        elif obstacle and snake.shield_active:
            snake.shield_active = False

        # Food collision
        food = self.collision.snake_eats_food(snake, self.foods)
        if food:
            snake.grow()
            self.scores[0] += int(food.points * snake.score_multiplier)
            self.foods.remove(food)
            if len(self.foods) == 0:
                self.spawn_food()

        # Power-up collision
        powerup = self.collision.snake_gets_powerup(snake, self.powerups)
        if powerup:
            self.apply_powerup(snake, powerup)
            self.powerups.remove(powerup)

        # Check game over
        if not snake.alive:
            self.is_game_over = True

    def spawn_obstacle(self):
        """Spawn a random obstacle based on current difficulty."""
        rand = random.random()
        if rand < STATIC_WALL_PROBABILITY:
            obstacle = StaticWall
        elif rand < STATIC_WALL_PROBABILITY + MOVING_WALL_PROBABILITY:
            obstacle = lambda: MovingWall(
                random.randint(1, self.grid_width - 2),
                random.randint(1, self.grid_height - 2)
            )
        elif rand < STATIC_WALL_PROBABILITY + MOVING_WALL_PROBABILITY + SPIKE_PROBABILITY:
            obstacle = Spike
        else:
            obstacle = Spiral

        if obstacle == Spike or obstacle == StaticWall:
            x, y = self.collision.get_random_empty_cell(self.snakes, self.obstacles, self.foods, self.powerups)
            self.obstacles.append(obstacle(x, y))
        else:
            x, y = self.collision.get_random_empty_cell(self.snakes, self.obstacles, self.foods, self.powerups)
            self.obstacles.append(obstacle())

    def spawn_powerup(self):
        """Spawn a random power-up."""
        powerup_types = [POWERUP_SPEED_BOOST, POWERUP_SHIELD, POWERUP_SCORE_MULTIPLIER, POWERUP_FREEZE]
        powerup_type = random.choice(powerup_types)
        x, y = self.collision.get_random_empty_cell(self.snakes, self.obstacles, self.foods, self.powerups)
        self.powerups.append(PowerUp(x, y, powerup_type))

    def apply_powerup(self, snake, powerup):
        """Apply power-up effect to snake."""
        if powerup.type == POWERUP_SPEED_BOOST:
            snake.speed = min(SNAKE_MAX_SPEED, snake.speed * POWERUP_SPEED_MULTIPLIER)
        elif powerup.type == POWERUP_SHIELD:
            snake.shield_active = True
        elif powerup.type == POWERUP_SCORE_MULTIPLIER:
            snake.score_multiplier = POWERUP_SCORE_MULTIPLIER

    def get_state(self):
        """Return game state."""
        return {
            'mode': MODE_TIME_ATTACK,
            'snakes': self.snakes,
            'foods': self.foods,
            'obstacles': self.obstacles,
            'score': self.scores[0],
            'time_remaining': max(0, self.time_limit - self.elapsed_time),
            'game_over': self.is_game_over
        }

    def is_over(self):
        """Check if game is over."""
        return self.is_game_over


class PuzzleMode(GameMode):
    """Pre-designed puzzle levels."""

    def __init__(self, width, height):
        self.current_level = 0
        self.levels = []
        self.load_levels()
        super().__init__(width, height)

    def load_levels(self):
        """Load puzzle levels from JSON files."""
        import json
        import os

        levels_dir = "assets/levels"
        if os.path.exists(levels_dir):
            for filename in sorted(os.listdir(levels_dir)):
                if filename.endswith('.json'):
                    with open(os.path.join(levels_dir, filename)) as f:
                        self.levels.append(json.load(f))

        # If no levels, create a simple default level
        if not self.levels:
            self.levels = [
                {
                    'name': 'Level 1',
                    'food_count': 5,
                    'obstacles': []
                }
            ]

    def reset(self):
        """Initialize puzzle mode."""
        if self.current_level >= len(self.levels):
            self.is_game_over = True
            return

        level = self.levels[self.current_level]
        self.snakes = [Snake(self.grid_width // 2, self.grid_height // 2, COLOR_RED)]
        self.foods = []
        self.powerups = []
        self.obstacles = []
        self.scores = [0]

        # Load level-specific obstacles
        for obstacle_data in level.get('obstacles', []):
            # Parse and create obstacles
            pass

        # Spawn required food
        for _ in range(level.get('food_count', 5)):
            self.spawn_food()

        self.is_game_over = False

    def spawn_food(self):
        """Spawn food."""
        x, y = self.collision.get_random_empty_cell(self.snakes, self.obstacles, self.foods, self.powerups)
        self.foods.append(Food(x, y, False))

    def update(self, dt, input_handler):
        """Update puzzle mode."""
        if self.is_game_over:
            return

        snake = self.snakes[0]

        # Handle input
        if input_handler.is_key_pressed(pygame.K_UP):
            snake.set_direction((0, -1))
        elif input_handler.is_key_pressed(pygame.K_DOWN):
            snake.set_direction((0, 1))
        elif input_handler.is_key_pressed(pygame.K_LEFT):
            snake.set_direction((-1, 0))
        elif input_handler.is_key_pressed(pygame.K_RIGHT):
            snake.set_direction((1, 0))

        # Update snake
        snake.update(dt)

        # Check collisions
        # Wall collision
        if self.collision.snake_hits_wall(snake):
            snake.alive = False

        # Obstacle collision (fixed obstacles in puzzle mode)
        is_spike, obstacle = self.collision.snake_hits_obstacle(snake, self.obstacles)
        if is_spike:
            snake.alive = False
        elif obstacle:
            snake.alive = False

        # Food collision
        food = self.collision.snake_eats_food(snake, self.foods)
        if food:
            snake.grow()
            self.scores[0] += int(food.points * snake.score_multiplier)
            self.foods.remove(food)

        # Check if all food eaten -> move to next level
        if len(self.foods) == 0:
            self.current_level += 1
            if self.current_level >= len(self.levels):
                # All levels completed
                self.is_game_over = True
            else:
                # Move to next level
                self.reset()

        # Check game over (snake died)
        if not snake.alive:
            self.is_game_over = True

    def get_state(self):
        """Return game state."""
        return {
            'mode': MODE_PUZZLE,
            'level': self.current_level + 1,
            'snakes': self.snakes,
            'foods': self.foods,
            'obstacles': self.obstacles,
            'score': self.scores[0],
            'game_over': self.is_game_over
        }

    def is_over(self):
        """Check if game is over."""
        return self.is_game_over
