# LAB1: Laya decisions in a grid maze

## Goal

Build a Python program that uses Laya to guide a robot from the start cell to
the goal. This lab focuses on describing state, selecting actions, and evaluating
decisions. The supplied environment uses a known maze and exact robot position.
It requires no sensors, localization, graphics, or wheel physics.

The robot models differential-drive movement in discrete steps: it turns in
place and moves forward one cell. It cannot move sideways.

## Supplied infrastructure

`maze.py` provides a `Maze` class with one fixed, solvable maze:

```text
#########
#S......#
#.#####.#
#...#...#
###.#.#.#
#.....#G#
#########
```

`#` means wall; `.` means free space. `S` and `G` mark the start and goal in
this diagram. In the returned grid, those cells contain `.`; their coordinates
are returned separately.

Coordinates are **zero-based `(row, column)`**, with `(0, 0)` at the top left.
Rows increase downward; columns increase to the right. The start is `(1, 1)`,
facing east; the goal is `(5, 7)`.

| Method | Behavior |
| --- | --- |
| `Maze()` | Create an environment at its starting state. |
| `get_state()` | Return a fresh dictionary containing the full maze and current state. |
| `step(action)` | Apply one action; return `True` if applied, or `False` if forward movement is blocked. |
| `reset()` | Restore the start position and east-facing heading; return `None`. |

The state format is:

```python
{
    "grid": ["#########", "#.......#", ...],  # List of row strings
    "position": (1, 1),                       # (row, column)
    "heading": "east",                        # north/east/south/west
    "goal": (5, 7),
}
```

Each snapshot is independent of the environment. Editing a returned dictionary
or grid list does not change the maze. Call `get_state()` again after an action
to obtain the updated state.

| Action | Effect |
| --- | --- |
| `forward` | Move one cell in the current heading if the destination is free. |
| `turn_left` | Rotate 90 degrees counterclockwise without moving. |
| `turn_right` | Rotate 90 degrees clockwise without moving. |
| `turn_around` | Rotate 180 degrees without moving. |

Blocked moves preserve both position and heading. Unknown actions raise
`ValueError` and preserve state. Reaching the goal does not automatically stop
the environment: your program must detect completion.

## Try the module

Use Python 3.10 or newer. The maze module needs only the standard library.
From the repository root:

```bash
cd LAB1
python3
```

Then enter:

```python
from maze import Maze

maze = Maze()
print(maze.get_state())

applied = maze.step("forward")
print(applied)                       # True
print(maze.get_state()["position"])  # (1, 2)

maze.step("turn_left")               # Now facing north
print(maze.step("forward"))          # False: wall ahead

maze.reset()
print(maze.get_state()["heading"])   # east
```

Create your student program in `LAB1/student.py` so it can use
`from maze import Maze`. Run it from `LAB1` with `python3 student.py`.

## What you implement

1. **Laya setup and integration.** Follow the [root README's uv setup](../README.md#basic-usage)
   and the [Laya documentation](https://github.com/NandhaKishorM/laya).
   Laya is not bundled with this infrastructure.
2. **State description.** Convert the maze, pose, and goal into clear text for
   the model. Explain the coordinate convention, wall symbols, and headings.
   You can derive nearby walls from the grid and include visit history.
3. **Action selection.** Ask Laya to select one of the four supported actions.
   Extract and validate its result before passing it to `step()`.
4. **Navigation loop.** Read state, select an action, apply it, and repeat.
   Stop when `state["position"] == state["goal"]`. Add a maximum action count
   so unsuccessful runs terminate. Count turns and blocked moves too.
5. **Failure handling and memory.** Handle model failures and invalid outputs;
   decide how to respond to blocked moves or repeated visits. The environment
   keeps pose, but it does not maintain your navigation history.
6. **Results.** Report whether the goal was reached, total actions, and blocked
   moves. Record enough of the state/action trace to explain an unsuccessful run.

Keep the environment rules in `maze.py` and your model calls and navigation
logic in your student program. This separates responsibilities and lets the
same maze run with different decision policies. There is no need for a class
hierarchy, interfaces, or additional frameworks for this lab.

## Expected outcome

Submit your student program and a short description of its input format,
decision logic, and observed results. The program should use Laya to select
actions, stop at the goal or action limit, and report failures clearly. Do not
hard-code the successful route or change the maze to make the run succeed.
Model success is something to measure, not an assumption.

## Check the supplied environment

From the repository root, run:

```bash
python3 -m unittest discover -s LAB1 -v
```

The tests verify movement, wall rejection, turning, invalid actions, snapshot
isolation, goal reachability, and reset. They do not evaluate Laya or student code.
