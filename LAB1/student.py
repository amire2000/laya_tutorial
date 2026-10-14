"""Let Laya choose actions in the supplied maze."""

from collections import deque
import sys

from loguru import logger

if __package__:
    from .main import render_maze
    from .maze import Maze
else:
    from main import render_maze
    from maze import Maze


QUESTIONS = {
    "action": {
        "type": "choice",
        "instructions": (
            "Choose one robot action to progress toward the goal through free cells. "
            "Avoid walls and repeated position/heading states in recent history. "
            "Turning changes heading only; it does not move the robot."
        ),
        "criteria": {
            "forward": "Move one cell along the current heading when it is free and useful.",
            "turn_left": "Turn 90 degrees counterclockwise toward a useful free direction.",
            "turn_right": "Turn 90 degrees clockwise toward a useful free direction.",
            "turn_around": "Turn 180 degrees to backtrack when the current route is unhelpful.",
        },
    }
}


def build_questions(state: dict) -> dict:
    """Offer movement or turns only toward adjacent open cells, without a route."""
    headings = ("north", "east", "south", "west")
    directions = ((-1, 0), (0, 1), (1, 0), (0, -1))
    row, col = state["position"]
    grid = state["grid"]
    criteria = {}
    for action, turn in (("forward", 0), ("turn_left", -1), ("turn_right", 1), ("turn_around", 2)):
        index = (headings.index(state["heading"]) + turn) % 4
        dr, dc = directions[index]
        nr, nc = row + dr, col + dc
        free = 0 <= nr < len(grid) and 0 <= nc < len(grid[nr]) and grid[nr][nc] != "#"
        if free:
            criteria[action] = QUESTIONS["action"]["criteria"][action]
    return {"action": {**QUESTIONS["action"], "criteria": criteria}}


def describe_state(state: dict, history) -> str:
    """Describe exact observations without computing a route for the model."""
    row, col = state["position"]
    grid = state["grid"]
    nearby = []
    for heading, dr, dc in (
        ("north", -1, 0), ("east", 0, 1), ("south", 1, 0), ("west", 0, -1)
    ):
        nr, nc = row + dr, col + dc
        free = 0 <= nr < len(grid) and 0 <= nc < len(grid[nr]) and grid[nr][nc] != "#"
        nearby.append(f"{heading}: {'free' if free else 'wall'}")
    return (
        "Coordinates are zero-based (row, column), with (0, 0) at top left. "
        "Rows increase southward; columns increase eastward. # is wall; . is free.\n"
        + "\n".join(grid)
        + f"\nRobot position: {state['position']}; heading: {state['heading']}."
        + f"\nGoal position: {state['goal']}."
        + "\nAdjacent cells: " + "; ".join(nearby)
        + "\nRecent outcomes (oldest first):\n" + ("\n".join(history) or "None yet.")
    )


def run(maze: Maze, router, max_actions: int = 100) -> dict:
    """Run a bounded experiment; the router is supplied so tests need no model."""
    history = deque(maxlen=8)
    actions = blocked = 0
    status = "action_limit"
    state = maze.get_state()
    print(render_maze(state))
    while state["position"] != state["goal"] and actions < max_actions:
        questions = build_questions(state)
        try:
            result = router.predict(describe_state(state, history), questions)
        except Exception:
            logger.exception("Laya prediction failed")
            status = "model_error"
            break
        try:
            action = result["answers"]["action"]["choice"]
        except (KeyError, TypeError):
            action = None
        if not isinstance(action, str) or action not in questions["action"]["criteria"]:
            logger.error("Invalid Laya action: {!r}", action)
            status = "invalid_response"
            break
        before = state
        applied = maze.step(action)
        actions += 1
        blocked += not applied
        state = maze.get_state()
        outcome = (
            f"{before['position']} facing {before['heading']}: {action} "
            f"({'applied' if applied else 'blocked'}) -> "
            f"{state['position']} facing {state['heading']}"
        )
        history.append(outcome)
        logger.info("Action {}: {}", actions, outcome)
        print(render_maze(state))
    if state["position"] == state["goal"]:
        status = "goal_reached"
    summary = {"status": status, "actions": actions, "blocked_moves": blocked}
    print(f"Result: {status}; actions: {actions}; blocked moves: {blocked}")
    return summary


def main() -> int:
    logger.remove()
    logger.add(
        sys.stderr,
        colorize=True,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | "
        "<cyan>{name}:{line}</cyan> | <level>{message}</level>",
    )
    try:
        from laya import Router

        router = Router()
    except Exception:
        logger.exception("Cannot initialize Laya; install dependencies with uv sync")
        print("Result: model_error; actions: 0; blocked moves: 0")
        return 1
    summary = run(Maze(), router)
    return 0 if summary["status"] == "goal_reached" else 1


if __name__ == "__main__":
    sys.exit(main())
