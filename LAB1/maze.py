"""A fixed grid maze. Students supply the navigation policy."""

_GRID = (
    "#########",
    "#.......#",
    "#.#####.#",
    "#...#...#",
    "###.#.#.#",
    "#.....#.#",
    "#########",
)
_START = (1, 1)
_GOAL = (5, 7)
_HEADINGS = ("north", "east", "south", "west")
_DIRECTIONS = ((-1, 0), (0, 1), (1, 0), (0, -1))


class Maze:
    """Own maze state and movement rules, independently of any decision model."""

    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        """Restore the start cell and east-facing heading."""
        self._position = _START
        self._heading = 1

    def get_state(self) -> dict:
        """Return an independent snapshot; coordinates are (row, column)."""
        return {
            "grid": list(_GRID),
            "position": self._position,
            "heading": _HEADINGS[self._heading],
            "goal": _GOAL,
        }

    def step(self, action: str) -> bool:
        """Apply one action; return False only when forward is blocked.

        Unknown actions raise ValueError without changing state.
        """
        if action not in ("forward", "turn_left", "turn_right", "turn_around"):
            raise ValueError(f"Unknown action: {action!r}")

        if action == "forward":
            row, col = self._position
            dr, dc = _DIRECTIONS[self._heading]
            row, col = row + dr, col + dc
            if not (0 <= row < len(_GRID) and 0 <= col < len(_GRID[0])):
                return False
            if _GRID[row][col] == "#":
                return False
            self._position = (row, col)
        else:
            turn = {"turn_left": -1, "turn_right": 1, "turn_around": 2}[action]
            self._heading = (self._heading + turn) % 4
        return True
