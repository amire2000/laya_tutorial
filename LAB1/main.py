"""Load and print the supplied maze."""

if __package__:
    from .maze import Maze
else:
    from maze import Maze


def render_maze(state: dict) -> str:
    """Overlay cyan robot and green goal markers; robot takes precedence."""
    grid = list(state["grid"])
    for key, marker in (("goal", "G"), ("position", "R")):
        row, col = state[key]
        grid[row] = grid[row][:col] + marker + grid[row][col + 1:]
    return "\n".join(grid).replace("R", "\033[96mR\033[0m").replace("G", "\033[92mG\033[0m")


def main() -> None:
    maze = Maze()
    print(render_maze(maze.get_state()))


if __name__ == "__main__":
    main()
