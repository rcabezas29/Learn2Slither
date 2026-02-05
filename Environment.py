from Snake import Snake
import numpy as np
from Action import Action


class Board:
    def __init__(self, width: int = 10, height: int = 10):
        ''''''
        self.width = width
        self.height = height
        self.grid = [[None for _ in range(width)] for _ in range(height)]

        # Generate green apples at non-overlapping positions
        self.green_apples = []
        while len(self.green_apples) < 2:
            apple = tuple(np.random.randint(0, self.width, 2))
            if apple not in self.green_apples:
                self.green_apples.append(apple)

        # Generate red apple at a position different from green apples
        while True:
            self.red_apple = tuple(np.random.randint(0, self.width, 2))
            if self.red_apple not in self.green_apples:
                break


class Environment:
    def __init__(self, size: int = 10):
        self.board = Board(width=size, height=size)

        # Generate snake at a position that doesn't overlap with apples
        occupied_positions = set(
            self.board.green_apples + [self.board.red_apple])

        while True:
            snake_head = (
                np.random.randint(
                    self.board.width / 4, self.board.width / 4 * 3
                ),
                np.random.randint(
                    self.board.height / 4, self.board.height / 4 * 3
                ),
            )

            # Try to create the snake
            self.snake = Snake(
                length=3,
                position=snake_head,
                board_width=self.board.width,
                board_height=self.board.height
            )

            # Check if any part of the snake overlaps with apples
            snake_positions = set(self.snake.body)
            if not snake_positions.intersection(occupied_positions):
                # No overlap, snake is valid
                break

    def execute_action(self, action: Action) -> float:
        new_head = list(self.snake.body[0])
        match action:
            case Action.UP:
                new_head[1] -= 1
            case Action.DOWN:
                new_head[1] += 1
            case Action.LEFT:
                new_head[0] -= 1
            case Action.RIGHT:
                new_head[0] += 1

        # Abort if the move would leave the board; the caller can catch this.
        if (new_head[0] < 0 or new_head[0] >= self.board.width or
                new_head[1] < 0 or new_head[1] >= self.board.height):
            raise Exception(
                f"Snake has collided with the wall! at position {new_head}"
            )

        # If the snake would bite itself, ignore the move.
        if tuple(new_head) in self.snake.body:
            raise Exception("Snake has bitten itself!")

        reward = -1  # Default movement penalty
        # Check for apple consumption
        if tuple(new_head) == self.board.red_apple:
            # For simplicity, just move the red apple to a new random position
            while True:
                new_red_apple = tuple(
                    np.random.randint(0, self.board.width, 2))
                self.snake.body.pop()  # Remove tail segment
                if self.snake.length == 0:
                    raise Exception("Snake has no length left!")
                if (new_red_apple not in self.board.green_apples and
                        new_red_apple not in self.snake.body):
                    self.board.red_apple = new_red_apple
                    reward = -10
                    break
        elif tuple(new_head) in self.board.green_apples:
            # Remove the green apple and grow the snake
            self.board.green_apples.remove(tuple(new_head))
            # Grow the snake by adding a new segment at the tail
            self.snake.body.append(self.snake.body[-1])  # Simple growth logic
            # Add a new green apple
            while True:
                new_green_apple = tuple(
                    np.random.randint(0, self.board.width, 2))
                if (new_green_apple != self.board.red_apple and
                    new_green_apple not in self.board.green_apples and
                        new_green_apple not in self.snake.body):
                    self.board.green_apples.append(new_green_apple)
                    reward = 10
                    break

        self.snake.update_position(tuple(new_head), action)
        return reward
