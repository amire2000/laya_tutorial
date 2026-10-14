# Laya Robotics Labs

Learn to use Laya for robot decision-making through small Python labs.
Each lab supplies an environment; students implement the model integration
and decision logic.

## What is Laya?

[Laya](https://github.com/NandhaKishorM/laya) is an open-source decision model
that answers structured choice, score, and yes/no questions about a text
description. For robotics, your program describes the robot's state and asks
the model to select an action. Your environment or controller executes it.

## Basic usage

Use Python 3.11 or newer and [install uv](https://docs.astral.sh/uv/getting-started/installation/).
From the repository root, install the project's declared dependencies:

```bash
uv sync
source .venv/bin/activate
```

A minimal choice request:

```python
from laya import Router

router = Router()
state = "The robot battery is critically low."
questions = {
    "action": {
        "type": "choice",
        "instructions": "What should the robot do?",
        "criteria": {
            "stop": "Battery is critically low.",
            "continue": "Battery is sufficient to continue.",
        },
    }
}

result = router.predict(state, questions)
print(result["answers"]["action"]["choice"])
```

The first prediction downloads model weights. Evaluate the decisions on your
task before relying on them. The supplied maze module works without Laya.

## Labs

| Lab | Description |
| --- | --- |
| [LAB1: Grid maze](LAB1/readme.md) | Use a fixed maze and full robot state to implement Laya action selection and a navigation loop. |

Run LAB1 from the repository root using uv:

```bash
uv run LAB1/main.py
```

This prints the maze with `R` marking the robot and `G` marking the goal.
The entry point does not require Laya.

Run the Laya navigation reference solution:

```bash
uv run LAB1/student.py
```

See the [LAB1 walkthrough](LAB1/readme.md#run-the-laya-solution) for the state
description, model request, movement diagrams, and how to evaluate results.

## Read more

- [Laya documentation](https://nandhakishorm.github.io/laya/): setup, prediction, and API reference.
- [Laya repository and quickstart](https://github.com/NandhaKishorM/laya#quickstart): usage and model details.
- [Laya examples](https://github.com/NandhaKishorM/laya/tree/main/examples): runnable examples.
