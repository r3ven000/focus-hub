# Focus Hub

A modular CLI tool for managing time, tasks, and habits.

**Focus Hub** is a personal productivity tool built around the Pomodoro Technique.
In the future, it will be expanded with task management, habit tracking, and personal reflection features.

## Functionality

### Ready-to-use features
- **Pomodoro Timer** — work sessions with customizable intervals
- **To-Do List** — task management alongside the timer
- **Habit Tracker** — habit tracking and development
- **Plugin System** — drop-in extensions for custom modules

### Features in development
- **Diary** — reflection on progress and the day
- **Data Export** — save to JSON or sync with Obsidian

## Plugins

Plugins are plain Python modules placed in the `extensions/` directory. They are
discovered and loaded automatically at startup and appear in the main menu.

```python
# extensions/my_tool.py
from core.plugins import register

@register(name="my tool", key="m", description="Does something neat")
def run(width):
    ...
```

- `name` — the label shown in the menu
- `key` — the single character users press to run it
- `description` — optional; falls back to the function docstring

Handlers receive the current terminal `width` and can persist state with
`core.storage` (`load` / `save`). Built-in features (pomodoro, to-do, settings)
are registered the same way through `core.plugins.load_builtins()`.

## Development

Run the test suite with:

```bash
pip install -r requirements.txt -r requirements-dev.txt
python -m pytest
```

Coverage report (same command used in CI):

```bash
python -m pytest --cov=core --cov=extensions --cov=cli --cov-report=term-missing
```

Static type checking (same command used in CI):

```bash
python -m mypy cli core extensions
```

## Vision

Start with a timer. Expand as needed.  Nothing extra—just what you use.

## Status

Early development. CLI is in the forefront, GUI is planned.