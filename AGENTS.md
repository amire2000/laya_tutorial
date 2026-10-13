# Repository Instructions

## Code Design

Create and modify code using SOLID design principles:

- **Single Responsibility:** Give each class or module one clear responsibility.
- **Open/Closed:** Support extensions without unnecessarily modifying existing behavior.
- **Liskov Substitution:** Ensure subtypes preserve the contracts of their base types.
- **Interface Segregation:** Keep interfaces focused so callers depend only on what they need.
- **Dependency Inversion:** Depend on abstractions where needed to decouple high-level logic from implementation details.

Apply these principles proportionately to the task; avoid unnecessary abstractions or design patterns.

## Logging

Use Loguru for application logging. Configure the console sink once at the entry
point with `colorize=True` and the following format, including date and time,
level, module name, line number, and a descriptive message:

```python
"<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <cyan>{name}:{line}</cyan> | <level>{message}</level>"
```

Remove Loguru's default sink before adding the configured sink to avoid duplicate
messages. Keep direct `print()` calls for program output such as the maze grid.
