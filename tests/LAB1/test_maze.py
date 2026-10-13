"""Checks for the supplied environment, not a student navigation solution."""

import unittest

from LAB1.maze import Maze


class MazeTests(unittest.TestCase):
    def test_initial_state_and_snapshot_isolation(self):
        maze = Maze()
        state = maze.get_state()
        self.assertEqual(state["position"], (1, 1))
        self.assertEqual(state["heading"], "east")
        self.assertEqual(state["goal"], (5, 7))
        state["grid"][1] = "#########"
        state["position"] = (0, 0)
        self.assertEqual(maze.get_state()["grid"][1], "#.......#")
        self.assertEqual(maze.get_state()["position"], (1, 1))

    def test_forward_and_blocked_move(self):
        maze = Maze()
        self.assertTrue(maze.step("forward"))
        self.assertEqual(maze.get_state()["position"], (1, 2))
        maze.step("turn_left")
        before = maze.get_state()
        self.assertFalse(maze.step("forward"))
        self.assertEqual(maze.get_state(), before)

    def test_turns_and_wraparound(self):
        maze = Maze()
        for action, heading in (
            ("turn_left", "north"),
            ("turn_left", "west"),
            ("turn_right", "north"),
            ("turn_around", "south"),
            ("turn_right", "west"),
            ("turn_right", "north"),
        ):
            with self.subTest(action=action, heading=heading):
                self.assertTrue(maze.step(action))
                self.assertEqual(maze.get_state()["heading"], heading)
                self.assertEqual(maze.get_state()["position"], (1, 1))

    def test_invalid_action_leaves_state_unchanged(self):
        maze = Maze()
        before = maze.get_state()
        with self.assertRaises(ValueError):
            maze.step("jump")
        self.assertEqual(maze.get_state(), before)

    def test_goal_is_reachable_and_reset_restores_start(self):
        maze = Maze()
        initial = maze.get_state()
        for _ in range(6):
            self.assertTrue(maze.step("forward"))
        maze.step("turn_right")
        for _ in range(4):
            self.assertTrue(maze.step("forward"))
        state = maze.get_state()
        self.assertEqual(state["position"], state["goal"])
        maze.reset()
        self.assertEqual(maze.get_state(), initial)


if __name__ == "__main__":
    unittest.main()
