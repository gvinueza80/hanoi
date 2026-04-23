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
