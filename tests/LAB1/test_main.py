"""Check the LAB1 entry point from the repository root."""

from pathlib import Path
import subprocess
import sys
import unittest

from LAB1.main import render_maze
from LAB1.maze import Maze


class MainTests(unittest.TestCase):
    def test_entry_point_prints_maze(self):
        root = Path(__file__).resolve().parents[2]
        result = subprocess.run(
            [sys.executable, "LAB1/main.py"],
            cwd=root,
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertEqual(
            result.stdout,
            "#########\n"
            "#R......#\n"
            "#.#####.#\n"
            "#...#...#\n"
            "###.#.#.#\n"
            "#.....#G#\n"
            "#########\n",
        )

    def test_render_tracks_robot_without_changing_snapshot(self):
        maze = Maze()
        maze.step("forward")
        state = maze.get_state()
        original_grid = list(state["grid"])
        self.assertEqual(render_maze(state).splitlines()[1], "#.R.....#")
        self.assertEqual(state["grid"], original_grid)

    def test_robot_at_goal_takes_precedence(self):
        state = Maze().get_state()
        state["position"] = state["goal"]
        rendered = render_maze(state)
        self.assertEqual(rendered.splitlines()[5], "#.....#R#")
        self.assertNotIn("G", rendered)


if __name__ == "__main__":
    unittest.main()
