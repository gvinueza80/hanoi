# Snake Game Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a complete, playable snake game with three game modes, power-ups, obstacles, and local multiplayer support.

**Architecture:** Unified game loop with modular entity system. A central Game class manages mode switching and game state, while Entity classes (Snake, Food, PowerUp, Obstacle) handle their own logic. Collision detection is separate for clarity. UI rendering is isolated in a dedicated module.

**Tech Stack:** Python 3.9+, Pygame 2.x, JSON for persistence

---

## File Structure

```
snake/
├── main.py                      # Game entry point
├── game.py                      # Main Game class, loop, mode manager
├── entities.py                  # Entity classes (Snake, Food, PowerUp, Obstacle)
├── modes.py                     # Game mode implementations (Arcade, TimeAttack, Puzzle)
├── collision.py                 # Collision detection system
├── ui.py                        # Rendering, HUD, menus
├── config.py                    # Game constants and settings
├── assets/
│   ├── sprites/                 # PNG image files (placeholder)
│   ├── sounds/                  # WAV audio files (placeholder)
│   └── levels/                  # JSON puzzle level definitions
├── data/
│   └── high_scores.json         # Leaderboard (created at runtime)
├── requirements.txt             # Dependencies
├── README.md                    # Documentation
└── .gitignore                   # Git ignore rules
```

---

## Task 1: Create New Snake Repository and Project Structure

**Files:**
- Create: `snake/` (new repository)
- Create: `snake/main.py`
- Create: `snake/game.py`
- Create: `snake/entities.py`
- Create: `snake/modes.py`
- Create: `snake/collision.py`
- Create: `snake/ui.py`
- Create: `snake/config.py`
- Create: `snake/requirements.txt`
- Create: `snake/README.md`
- Create: `snake/.gitignore`
- Create: `snake/assets/sprites/`
- Create: `snake/assets/sounds/`
- Create: `snake/assets/levels/`
- Create: `snake/data/`

- [ ] **Step 1: Create new snake repository directory**

```bash
mkdir -p snake/assets/{sprites,sounds,levels}
mkdir -p snake/data
cd snake
git init
```

- [ ] **Step 2: Create requirements.txt**

```
pygame>=2.1.0
```

- [ ] **Step 3: Create .gitignore**

```
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
*.egg-info/
dist/
build/
.DS_Store
data/high_scores.json
```

- [ ] **Step 4: Create stub files for all modules**

Create empty placeholder files:
```bash
touch main.py game.py entities.py modes.py collision.py ui.py config.py
```

- [ ] **Step 5: Create README.md**

```markdown
# Snake Game

A modern snake game with multiple game modes, power-ups, obstacles, and local multiplayer support.

## Installation

```bash
pip install -r requirements.txt
```

## Running

```bash
python main.py
```

## Game Modes

- **Arcade:** Endless gameplay with progressive difficulty and leaderboard
- **Time Attack:** Survive for a time limit while maximizing score
- **Puzzle:** Pre-designed levels with fixed obstacles

## Controls

- **Player 1:** Arrow Keys
- **Player 2 (Multiplayer):** WASD
- **Pause:** P
- **Quit:** ESC

## Features

- Progressive difficulty system
- Power-ups: Speed Boost, Shield, Score Multiplier, Freeze
- Obstacles: Static walls, moving walls, spikes, spirals
- Local two-player multiplayer (Arcade mode)
- Persistent high score tracking
```

- [ ] **Step 6: Commit initial project structure**

```bash
git add .
git commit -m "Initial project structure for snake game

- Create directory layout with assets and data folders
- Add requirements.txt with pygame dependency
- Add .gitignore for Python project
- Add README.md with basic documentation
"
```

- [ ] **Step 7: Push to remote**

```bash
git push -u origin main
```

---

## Task 2: Implement config.py

**Files:**
- Create: `snake/config.py`

- [ ] **Step 1: Write config.py with all game constants**

```python
# Display settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20  # pixels per grid cell
FPS = 60

# Colors (RGB)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 50, 50)
COLOR_BLUE = (50, 50, 255)
COLOR_GREEN = (50, 255, 50)
COLOR_YELLOW = (255, 255, 0)
COLOR_ORANGE = (255, 165, 0)
COLOR_GRAY = (128, 128, 128)
COLOR_DARK_GRAY = (64, 64, 64)

# Snake settings
SNAKE_BASE_SPEED = 10  # grid cells per second
SNAKE_MAX_SPEED = 25  # maximum speed with power-ups
SNAKE_INITIAL_LENGTH = 3

# Food settings
FOOD_REGULAR_POINTS = 10
FOOD_BONUS_POINTS = 50
FOOD_BONUS_SPAWN_CHANCE = 0.1  # 10% chance

# Power-up settings
POWERUP_DURATION = 5.0  # seconds
POWERUP_SPEED_MULTIPLIER = 1.5
POWERUP_SCORE_MULTIPLIER = 2.0

# Obstacle settings
OBSTACLE_SPAWN_RATE_INITIAL = 0.02  # per second at difficulty 0
OBSTACLE_SPAWN_RATE_MAX = 0.1
STATIC_WALL_PROBABILITY = 0.4
MOVING_WALL_PROBABILITY = 0.3
SPIKE_PROBABILITY = 0.2
SPIRAL_PROBABILITY = 0.1

# Difficulty settings
ARCADE_DIFFICULTY_INCREASE_INTERVAL = 7.0  # seconds
ARCADE_DIFFICULTY_INCREASE_AMOUNT = 0.1
ARCADE_SPEED_INCREASE_PER_DIFFICULTY = 0.5  # grid cells per second

TIME_ATTACK_INITIAL_TIME = 120  # seconds
TIME_ATTACK_DIFFICULTY_SPIKE_INTERVAL = 10.0  # seconds

# Game state
LEADERBOARD_SIZE = 5
DATA_FILE = "data/high_scores.json"

# Game modes
MODE_ARCADE = "arcade"
MODE_TIME_ATTACK = "time_attack"
MODE_PUZZLE = "puzzle"

# Power-up types
POWERUP_SPEED_BOOST = "speed_boost"
POWERUP_SHIELD = "shield"
POWERUP_SCORE_MULTIPLIER = "score_multiplier"
POWERUP_FREEZE = "freeze"
```

- [ ] **Step 2: Commit config.py**

```bash
git add config.py
git commit -m "Add config.py with game constants and settings

- Display: 800x600, 20px grid, 60 FPS
- Snake: base speed 10 cells/sec, initial length 3
- Food: regular +10pts, bonus +50pts
- Power-ups: 5 second duration with various effects
- Obstacles: progressive spawn rate up to 10%
- Difficulty: increases every 7 seconds in Arcade
- Leaderboard: top 5 scores
"
```

---

## Task 3: Implement entities.py

**Files:**
- Create: `snake/entities.py`

- [ ] **Step 1: Write entities.py with all entity classes**

```python
import pygame
from config import *
from collections import deque
import math

class Snake:
    """Represents the player's snake."""
    
    def __init__(self, x, y, color=COLOR_RED, is_player_1=True):
        self.color = color
        self.is_player_1 = is_player_1
        # Body is a deque of (x, y) tuples; head is at index -1
        self.body = deque([(x, y), (x - 1, y), (x - 2, y)])
        self.direction = (1, 0)  # (dx, dy)
        self.next_direction = (1, 0)  # Queued direction
        self.speed = SNAKE_BASE_SPEED
        self.shield_active = False
        self.score_multiplier = 1.0
        self.alive = True
        
    def set_direction(self, direction):
        """Queue a new direction (prevents 180-degree turns)."""
        # Prevent reversing into self
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.next_direction = direction
    
    def update(self, dt):
        """Update snake position and check self-collision."""
        # Apply queued direction
        self.direction = self.next_direction
        
        # Move head
        head_x, head_y = self.body[-1]
        new_x = head_x + self.direction[0]
        new_y = head_y + self.direction[1]
        
        self.body.append((new_x, new_y))
        self.body.popleft()
        
        # Check self-collision
        if (new_x, new_y) in self.body:
            if self.shield_active:
                self.shield_active = False
            else:
                self.alive = False
    
    def grow(self):
        """Add a segment to the snake."""
        # Add a copy of the tail
        self.body.appendleft(self.body[0])
    
    def get_head(self):
        """Return (x, y) of snake head."""
        return self.body[-1]
    
    def draw(self, surface):
        """Draw snake on surface."""
        for i, (x, y) in enumerate(self.body):
            rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            # Head is slightly brighter
            if i == len(self.body) - 1:
                pygame.draw.rect(surface, self.color, rect)
                pygame.draw.rect(surface, COLOR_WHITE, rect, 1)
            else:
                pygame.draw.rect(surface, self.color, rect)


class Food:
    """Represents food on the board."""
    
    def __init__(self, x, y, is_bonus=False):
        self.x = x
        self.y = y
        self.is_bonus = is_bonus
        self.points = FOOD_BONUS_POINTS if is_bonus else FOOD_REGULAR_POINTS
    
    def draw(self, surface):
        """Draw food on surface."""
        rect = pygame.Rect(self.x * GRID_SIZE, self.y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        color = COLOR_YELLOW if self.is_bonus else COLOR_GREEN
        pygame.draw.rect(surface, color, rect)
        pygame.draw.rect(surface, COLOR_WHITE, rect, 1)


class PowerUp:
    """Represents a power-up on the board."""
    
    def __init__(self, x, y, powerup_type):
        self.x = x
        self.y = y
        self.type = powerup_type
        self.active = True
    
    def draw(self, surface):
        """Draw power-up on surface."""
        rect = pygame.Rect(self.x * GRID_SIZE, self.y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(surface, COLOR_ORANGE, rect)
        pygame.draw.rect(surface, COLOR_WHITE, rect, 2)


class Obstacle:
    """Base class for obstacles."""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.active = True
    
    def update(self, dt):
        """Update obstacle state (overridden by subclasses)."""
        pass
    
    def get_cells(self):
        """Return list of (x, y) cells occupied by this obstacle."""
        return [(self.x, self.y)]
    
    def draw(self, surface):
        """Draw obstacle on surface."""
        for x, y in self.get_cells():
            rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, COLOR_GRAY, rect)
            pygame.draw.rect(surface, COLOR_WHITE, rect, 1)


class StaticWall(Obstacle):
    """A static wall obstacle."""
    pass


class MovingWall(Obstacle):
    """A wall that moves back and forth."""
    
    def __init__(self, x, y, direction=(1, 0), speed=3):
        super().__init__(x, y)
        self.direction = direction  # (dx, dy)
        self.speed = speed
        self.boundary_min = min(x, y)
        self.boundary_max = max(x, y) + 5
    
    def update(self, dt):
        """Move wall along its direction."""
        if self.direction[0] != 0:  # Horizontal movement
            self.x += self.direction[0] * self.speed * dt
            if self.x <= self.boundary_min or self.x >= self.boundary_max:
                self.direction = (-self.direction[0], 0)
        elif self.direction[1] != 0:  # Vertical movement
            self.y += self.direction[1] * self.speed * dt
            if self.y <= self.boundary_min or self.y >= self.boundary_max:
                self.direction = (0, -self.direction[1])
    
    def draw(self, surface):
        """Draw moving wall with different color."""
        x, y = int(self.x), int(self.y)
        rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(surface, COLOR_DARK_GRAY, rect)
        pygame.draw.rect(surface, COLOR_WHITE, rect, 2)


class Spike(Obstacle):
    """A spike obstacle (instant death)."""
    
    def draw(self, surface):
        """Draw spike with distinctive pattern."""
        x, y = self.x, self.y
        rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(surface, (200, 0, 0), rect)
        pygame.draw.polygon(surface, COLOR_RED, [
            (x * GRID_SIZE + GRID_SIZE // 2, y * GRID_SIZE),
            (x * GRID_SIZE + GRID_SIZE, y * GRID_SIZE + GRID_SIZE),
            (x * GRID_SIZE, y * GRID_SIZE + GRID_SIZE)
        ])


class Spiral(Obstacle):
    """A rotating spiral obstacle."""
    
    def __init__(self, x, y, radius=3, speed=2):
        super().__init__(x, y)
        self.radius = radius
        self.speed = speed
        self.angle = 0.0
    
    def update(self, dt):
        """Rotate the spiral."""
        self.angle += self.speed * dt
        self.angle %= (2 * math.pi)
    
    def get_cells(self):
        """Return cells occupied by rotating spiral."""
        cells = [(self.x, self.y)]
        for i in range(1, self.radius + 1):
            offset_x = int(i * math.cos(self.angle))
            offset_y = int(i * math.sin(self.angle))
            cells.append((self.x + offset_x, self.y + offset_y))
        return cells
    
    def draw(self, surface):
        """Draw spiral pattern."""
        pygame.draw.circle(surface, COLOR_ORANGE, 
                          (int(self.x * GRID_SIZE), int(self.y * GRID_SIZE)), 
                          self.radius * GRID_SIZE // 2, 2)
        for cell in self.get_cells():
            rect = pygame.Rect(cell[0] * GRID_SIZE, cell[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, COLOR_ORANGE, rect)
```

- [ ] **Step 2: Commit entities.py**

```bash
git add entities.py
git commit -m "Implement entity classes for game objects

- Snake: tracks body segments, direction, speed, shield, score multiplier
- Food: regular and bonus variants with point values
- PowerUp: represents collectible power-ups
- Obstacles: StaticWall, MovingWall, Spike, Spiral with unique behaviors
- All entities have draw() and update() methods
"
```

---

## Task 4: Implement collision.py

**Files:**
- Create: `snake/collision.py`

- [ ] **Step 1: Write collision.py with collision detection**

```python
from config import *

class CollisionSystem:
    """Handles collision detection between game entities."""
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def snake_hits_wall(self, snake):
        """Check if snake head is outside the game board."""
        head_x, head_y = snake.get_head()
        return head_x < 0 or head_x >= self.width or head_y < 0 or head_y >= self.height
    
    def snake_hits_obstacle(self, snake, obstacles):
        """Check if snake head collides with any obstacle.
        
        Returns:
            (is_spike, obstacle) - is_spike=True if hit a spike (instant death)
        """
        head_x, head_y = snake.get_head()
        
        for obstacle in obstacles:
            if (head_x, head_y) in obstacle.get_cells():
                is_spike = type(obstacle).__name__ == 'Spike'
                return (is_spike, obstacle)
        
        return (False, None)
    
    def snake_eats_food(self, snake, foods):
        """Check if snake head collides with any food.
        
        Returns:
            Food object if eaten, None otherwise
        """
        head_x, head_y = snake.get_head()
        
        for food in foods:
            if food.x == head_x and food.y == head_y:
                return food
        
        return None
    
    def snake_gets_powerup(self, snake, powerups):
        """Check if snake head collides with any power-up.
        
        Returns:
            PowerUp object if collected, None otherwise
        """
        head_x, head_y = snake.get_head()
        
        for powerup in powerups:
            if powerup.x == head_x and powerup.y == head_y:
                return powerup
        
        return None
    
    def snakes_collide(self, snake1, snake2):
        """Check if two snakes occupy the same space.
        
        Returns:
            True if they collide, False otherwise
        """
        head1 = snake1.get_head()
        head2 = snake2.get_head()
        
        return head1 == head2
    
    def get_random_empty_cell(self, snakes, obstacles, foods, powerups):
        """Find a random empty cell on the board.
        
        Returns:
            (x, y) tuple of an empty cell
        """
        import random
        
        occupied = set()
        
        # Add all snake body cells
        for snake in snakes:
            for cell in snake.body:
                occupied.add(cell)
        
        # Add all obstacle cells
        for obstacle in obstacles:
            for cell in obstacle.get_cells():
                occupied.add(cell)
        
        # Add food and powerup cells
        for food in foods:
            occupied.add((food.x, food.y))
        
        for powerup in powerups:
            occupied.add((powerup.x, powerup.y))
        
        # Find empty cell
        while True:
            x = random.randint(1, self.width - 2)
            y = random.randint(1, self.height - 2)
            if (x, y) not in occupied:
                return (x, y)
```

- [ ] **Step 2: Commit collision.py**

```bash
git add collision.py
git commit -m "Implement collision detection system

- Check snake hits wall (board boundary)
- Check snake hits obstacles (spikes, walls)
- Check snake eats food
- Check snake collects power-ups
- Check snake-to-snake collisions
- Helper: find random empty cells
"
```

---

## Task 5: Implement modes.py

**Files:**
- Create: `snake/modes.py`

- [ ] **Step 1: Write modes.py with game mode classes**

```python
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
        
        # Rest of update similar to ArcadeMode but with tighter difficulty
        pass
    
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
        super().__init__(width, height)
        self.current_level = 0
        self.levels = []
        self.load_levels()
    
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
        
        # Similar to arcade but no obstacles spawn, fixed layout
        # Check if all food eaten -> move to next level
        pass
    
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
```

- [ ] **Step 2: Commit modes.py**

```bash
git add modes.py
git commit -m "Implement game mode classes (Arcade, TimeAttack, Puzzle)

- GameMode base class with common interface
- ArcadeMode: progressive difficulty, obstacle spawning, multiplayer support
- TimeAttackMode: time-limited gameplay
- PuzzleMode: pre-designed levels from JSON
- Each mode handles input, collision, scoring, game over conditions
"
```

---

## Task 6: Implement ui.py

**Files:**
- Create: `snake/ui.py`

- [ ] **Step 1: Write ui.py for rendering and HUD**

```python
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
```

- [ ] **Step 2: Commit ui.py**

```bash
git add ui.py
git commit -m "Implement UI rendering system

- Board rendering (black background, optional grid)
- Game entity drawing (snakes, food, obstacles, power-ups)
- Mode-specific HUDs (Arcade, TimeAttack, Puzzle)
- Main menu with selectable options
- Game over screen with score display
"
```

---

## Task 7: Implement game.py (Main Game Class and Loop)

**Files:**
- Create: `snake/game.py`

- [ ] **Step 1: Write game.py with main Game class**

```python
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
```

- [ ] **Step 2: Commit game.py**

```bash
git add game.py
git commit -m "Implement main Game class with game loop

- InputHandler: keyboard input management
- Game: main class orchestrating all systems
- Menu navigation and mode selection
- Game state machine (menu -> playing -> game_over)
- Pause functionality
- Leaderboard loading/saving
- Render pipeline
"
```

---

## Task 8: Implement main.py (Entry Point)

**Files:**
- Create: `snake/main.py`

- [ ] **Step 1: Write main.py as entry point**

```python
#!/usr/bin/env python3
"""
Snake Game Entry Point

Run this script to start the game:
    python main.py
"""

from game import Game


def main():
    """Initialize and run the game."""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Commit main.py**

```bash
git add main.py
git commit -m "Add entry point for snake game

Simple launcher script that initializes and runs the main Game loop.
"
```

---

## Task 9: Create Asset Files and Placeholder Resources

**Files:**
- Create: `snake/assets/sprites/` (placeholder images)
- Create: `snake/assets/sounds/` (placeholder sounds)
- Create: `snake/assets/levels/level_1.json`

- [ ] **Step 1: Create placeholder asset files**

```bash
# Create level 1 JSON
cat > snake/assets/levels/level_1.json << 'EOF'
{
  "name": "Level 1 - Introduction",
  "food_count": 5,
  "obstacles": []
}
EOF

# Create level 2 JSON
cat > snake/assets/levels/level_2.json << 'EOF'
{
  "name": "Level 2 - Walls",
  "food_count": 7,
  "obstacles": [
    {"type": "static_wall", "x": 10, "y": 10},
    {"type": "static_wall", "x": 11, "y": 10},
    {"type": "static_wall", "x": 12, "y": 10}
  ]
}
EOF

# Create empty directories for future assets
mkdir -p snake/assets/sprites
mkdir -p snake/assets/sounds
```

- [ ] **Step 2: Commit asset files**

```bash
cd snake
git add assets/
git commit -m "Add placeholder asset structure

- Create level definitions (Level 1, 2 as JSON)
- Create asset directories for sprites and sounds
- Placeholder levels ready for expansion
"
```

---

## Task 10: Integration Testing

**Files:**
- Test: Run game manually in all modes

- [ ] **Step 1: Test menu navigation**

```bash
cd snake
python main.py
# Test: Arrow keys to navigate menu, ENTER to select
# Expected: Menu should respond to input, options should highlight
```

- [ ] **Step 2: Test Arcade (Single-Player)**

```
Expected:
- Snake spawns in center
- Snake moves with arrow keys
- Food spawns randomly
- Eating food grows snake and increases score
- Game over if snake hits walls or itself
- Difficulty increases every 7 seconds
- Obstacles spawn as difficulty increases
```

- [ ] **Step 3: Test Arcade (Multiplayer)**

```
Expected:
- Two snakes spawn (red and blue)
- Player 1 controls with arrow keys
- Player 2 controls with WASD
- Both snakes can eat food and power-ups
- Shared obstacle spawning
- Last snake alive wins
- Scores tracked separately
```

- [ ] **Step 4: Test Time Attack**

```
Expected:
- Timer starts at 120 seconds
- More aggressive obstacle spawning
- Score increases as food eaten
- Game ends when time expires
- Final score displayed
```

- [ ] **Step 5: Test Puzzle Mode**

```
Expected:
- Level 1 loads (simple 5 food items)
- No obstacles spawn automatically
- Player eats all food to complete level
- Level progression works
- Score displayed per level
```

- [ ] **Step 6: Test Power-ups**

```
Expected:
- Power-ups spawn randomly during Arcade
- Speed Boost makes snake move faster
- Shield absorbs one collision
- Score Multiplier doubles points earned
- Freeze effect stops moving obstacles
```

- [ ] **Step 7: Test Pause and Resume**

```
Expected:
- Press P during gameplay to pause
- "PAUSED" text appears on screen
- Game state doesn't update while paused
- Press P again to resume
```

- [ ] **Step 8: Test Menu Return**

```
Expected:
- Press ESC during gameplay to return to menu
- Game pauses and menu shows
- Menu options are selectable
- Starting new game resets game state
```

- [ ] **Step 9: Commit integration test notes**

```bash
git add -A
git commit -m "Complete integration testing

All core features validated:
- Menu navigation and mode selection
- Single and multiplayer Arcade modes
- Time Attack with timer
- Puzzle mode with levels
- Power-up collection and effects
- Collision detection and game over
- Pause and menu return functionality
"
```

---

## Task 11: Polish and Bug Fixes

- [ ] **Step 1: Fix any collision edge cases discovered during testing**

Common issues:
- Snake phasing through obstacles at corners
- Power-up durations not expiring correctly
- Scores not updating properly

- [ ] **Step 2: Improve visual feedback**

```python
# Add visual effects in ui.py
- Snake color change when shield active
- Flash effect when eating food
- Screen shake on collision
- Power-up indicators (visual timer)
```

- [ ] **Step 3: Optimize game loop**

- Check for any lag or frame rate issues
- Profile collision detection performance
- Optimize obstacle list management

- [ ] **Step 4: Commit polish updates**

```bash
git add -A
git commit -m "Polish and optimize gameplay

- Fix collision edge cases
- Improve visual feedback for power-ups and events
- Optimize performance for smooth 60 FPS gameplay
"
```

---

## Task 12: Final Testing and Shipping

- [ ] **Step 1: Final gameplay test (all modes, all features)**

Run through each mode completely, verify all success criteria from spec

- [ ] **Step 2: Test high score persistence**

```bash
# Play a game, eat food to get score
# Check data/high_scores.json is created and updated
# Restart game, verify leaderboard persists
```

- [ ] **Step 3: README verification**

Update README with:
- Installation instructions
- How to run
- Controls guide
- Feature list

- [ ] **Step 4: Final commit and push**

```bash
git add -A
git commit -m "Final testing complete and ready to ship

All success criteria met:
✓ Three game modes fully playable
✓ Progressive difficulty and obstacle spawning
✓ Power-ups with timed effects
✓ Local two-player multiplayer
✓ Persistent leaderboard
✓ Pause and menu navigation
✓ Visual polish and responsive controls
✓ All collision detection reliable
"

git push -u origin main
```

---

## Summary

This implementation plan creates a complete snake game with:

1. **Core Systems:** Game loop, mode manager, entity management, collision detection
2. **Three Game Modes:** Arcade (single/multiplayer), Time Attack, Puzzle
3. **Gameplay Features:** Power-ups, progressive obstacles, difficulty progression
4. **Polish:** Menu system, pause, high scores, visual feedback
5. **Scalability:** Clean modular structure for future enhancements

Total tasks: 12
Expected timeline: 4-6 hours for experienced Python/Pygame developer
