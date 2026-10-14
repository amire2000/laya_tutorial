"""Exercise navigation without downloading or running model weights."""

from contextlib import redirect_stdout
from io import StringIO
import unittest
from unittest.mock import patch

from LAB1.maze import Maze
from LAB1.student import describe_state, run


class FakeRouter:
    def __init__(self, choices):
        self.choices = iter(choices)
        self.observations = []

    def predict(self, state, questions):
        self.observations.append(state)
        return {"answers": {"action": {"choice": next(self.choices)}}}


class StudentTests(unittest.TestCase):
    def setUp(self):
        self.output = StringIO()
        self.enterContext(redirect_stdout(self.output))
        self.logs = self.enterContext(patch("LAB1.student.logger"))

    def test_goal_completion(self):
        # This route is a test fixture, not a policy supplied to Laya.
        router = FakeRouter(["forward"] * 6 + ["turn_right"] + ["forward"] * 4)
        self.assertEqual(run(Maze(), router, max_actions=11), {
            "status": "goal_reached", "actions": 11, "blocked_moves": 0,
        })
        self.assertEqual(len(router.observations), 11)
        self.assertIn("#.....#\033[96mR\033[0m#", self.output.getvalue())

    def test_blocked_move_updates_history_and_counts(self):
        maze = Maze()
        router = FakeRouter(["forward"] * 3)
        step = maze.step
        attempts = 0

        def reject_second_move(action):
            nonlocal attempts
            attempts += 1
            return False if attempts == 2 else step(action)

        with patch.object(maze, "step", side_effect=reject_second_move):
            summary = run(maze, router, max_actions=3)
        self.assertEqual(summary, {
            "status": "action_limit", "actions": 3, "blocked_moves": 1,
        })
        self.assertEqual(maze.get_state()["position"], (1, 3))
        self.assertIn("Robot position: (1, 2)", router.observations[1])
        self.assertIn("forward (blocked)", router.observations[2])

    def test_repeated_turns_stop_at_limit_and_history_is_bounded(self):
        router = FakeRouter(["turn_right", "turn_left"] * 6)
        summary = run(Maze(), router, max_actions=12)
        self.assertEqual(summary["status"], "action_limit")
        self.assertEqual(summary["actions"], 12)
        history = router.observations[-1].split("Recent outcomes (oldest first):\n")[1]
        self.assertEqual(len(history.splitlines()), 8)

    def test_invalid_choices_do_not_move_maze(self):
        for choice in ("jump", None, ["forward"], "turn_left"):
            with self.subTest(choice=choice):
                maze = Maze()
                initial = maze.get_state()
                summary = run(maze, FakeRouter([choice]))
                self.assertEqual(summary["status"], "invalid_response")
                self.assertEqual(summary["actions"], 0)
                self.assertEqual(maze.get_state(), initial)

    def test_missing_response_fields_are_rejected(self):
        with patch.object(FakeRouter, "predict", return_value={}):
            self.assertEqual(run(Maze(), FakeRouter([]))["status"], "invalid_response")

    def test_model_exception_ends_run(self):
        with patch.object(FakeRouter, "predict", side_effect=RuntimeError("offline")):
            self.assertEqual(run(Maze(), FakeRouter([])), {
                "status": "model_error", "actions": 0, "blocked_moves": 0,
            })
        self.logs.exception.assert_called_once()

    def test_description_updates_observations(self):
        maze = Maze()
        self.assertIn("east: free; south: free; west: wall", describe_state(maze.get_state(), []))
        maze.step("forward")
        text = describe_state(maze.get_state(), [])
        self.assertIn("Robot position: (1, 2); heading: east", text)
        self.assertIn("south: wall", text)
        self.assertIn("Goal position: (5, 7)", text)

    def test_wall_corner_offers_only_turns_toward_open_cells(self):
        maze = Maze()
        for _ in range(6):
            maze.step("forward")
        with patch.object(FakeRouter, "predict", return_value={
            "answers": {"action": {"choice": "turn_right"}},
        }) as predict:
            run(maze, FakeRouter([]), max_actions=1)
        criteria = predict.call_args.args[1]["action"]["criteria"]
        self.assertEqual(set(criteria), {"turn_right", "turn_around"})
        self.assertEqual(maze.get_state()["heading"], "south")


if __name__ == "__main__":
    unittest.main()
