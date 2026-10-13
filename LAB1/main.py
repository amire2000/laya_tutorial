"""Load and print the supplied maze."""

if __package__:
    from .maze import Maze
else:
    from maze import Maze


def render_maze(state: dict) -> str:
    """Overlay the goal and robot on a copy of the grid; robot takes precedence."""
    grid = list(state["grid"])
    for key, marker in (("goal", "G"), ("position", "R")):
        row, col = state[key]
        grid[row] = grid[row][:col] + marker + grid[row][col + 1:]
    return "\n".join(grid)


def main() -> None:
    maze = Maze()
    print(render_maze(maze.get_state()))


if __name__ == "__main__":
    main()
