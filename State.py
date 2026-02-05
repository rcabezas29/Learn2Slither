from enum import Enum
from Environment import Environment


class Cell(Enum):
    EMPTY = "0"
    WALL = "W"
    HEAD = "H"
    BODY = "S"
    GREEN = "G"
    RED = "R"


DIRECTIONS = {
    "UP":    (0, -1),
    "LEFT":  (-1, 0),
    "DOWN":  (0, 1),
    "RIGHT": (1, 0),
}


class State:
    """
    Computes the snake vision in the 4 directions from its head.
    """

    ORDER = ("UP", "LEFT", "DOWN", "RIGHT")

    def __init__(self, environment: Environment):
        """
        board is expected to expose:
          - width, height
          - snake.head -> (x, y)
          - snake.body -> iterable of (x, y) INCLUDING head or not (both ok)
          - green_apples -> set of (x, y)
          - red_apples   -> set of (x, y)
        """
        self.observations = self.vision(environment)
        snake_direction = environment.snake.direction
        for name, (dx, dy) in DIRECTIONS.items():
            if (dx, dy) == snake_direction:
                self.direction = name
                break

    # ---------- low-level helpers ----------

    def _in_bounds(self, x, y, board):
        return 0 <= x < board.width and 0 <= y < board.height

    def _cell_at(self, x, y, environment: Environment):
        """
        Translate board contents into the subject symbols.
        """
        if not self._in_bounds(x, y, environment.board):
            return Cell.WALL.value

        if (x, y) == environment.snake.body[0]:
            return Cell.HEAD.value

        if (x, y) in environment.snake.body:
            return Cell.BODY.value

        if (x, y) in environment.board.green_apples:
            return Cell.GREEN.value

        if (x, y) == environment.board.red_apple:
            return Cell.RED.value

        return Cell.EMPTY.value

    # ---------- vision ----------

    def _ray(self, dx, dy, environment: Environment):
        """
        Return the list of symbols seen in one direction,
        starting NEXT to the head, until a wall is reached (wall included).
        """
        hx, hy = environment.snake.body[0]
        x, y = hx + dx, hy + dy

        result = []

        while True:
            if not self._in_bounds(x, y, environment.board):
                result.append(Cell.WALL.value)
                break

            c = self._cell_at(x, y, environment)
            result.append(c)

            x += dx
            y += dy

        return result

    def vision(self, environment: Environment):
        """
        Returns a dict:
            {
              "UP":    [...],
              "LEFT":  [...],
              "DOWN":  [...],
              "RIGHT": [...]
            }
        """
        out = {}
        for name in self.ORDER:
            dx, dy = DIRECTIONS[name]
            out[name] = self._ray(dx, dy, environment)
        return out

    def update(self, environment: Environment):
        """
        Update the observations based on the current environment state.
        """
        self.observations = self.vision(environment)
        snake_direction = (
            environment.snake.direction[0], environment.snake.direction[1])
        for name, (dx, dy) in DIRECTIONS.items():
            if (dx, dy) == snake_direction:
                self.direction = name
                break

    # ---------- representations ----------

    def as_tuple(self):
        """
        Hashable representation for Q-learning.

        Example:
        (
          ('0','0','G','W'),
          ('S','0','W'),
          ('0','0','0','W'),
          ('R','0','W')
        )
        """
        return tuple(tuple(self.observations[d]) for d in self.ORDER)

    def pretty_print(self):
        """
        Human-readable terminal output.
        """
        for d in self.ORDER:
            print(f"{d:5}: {' '.join(self.observations[d])}")
