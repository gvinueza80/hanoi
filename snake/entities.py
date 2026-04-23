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
        # Body laid out: tail -> ... -> head, where head is at higher x
        self.body = deque([(x - 2, y), (x - 1, y), (x, y)])
        self.direction = (1, 0)  # (dx, dy) - moving right (towards increasing x)
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

        # Check self-collision before moving (collision with existing body)
        if (new_x, new_y) in self.body:
            if self.shield_active:
                self.shield_active = False
            else:
                self.alive = False
            # Don't return - still need to update body for consistency

        self.body.append((new_x, new_y))
        self.body.popleft()

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
