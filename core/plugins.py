"""Plugin discovery and registration for Focus Hub.

Any module placed in ``extensions/`` can register itself as a plugin::

    from core.plugins import register

    @register(name="my tool", key="m", description="Does something neat")
    def run(width):
        ...

Extensions are discovered and imported at startup. Their handlers are
merged into the main menu. A handler receives the current terminal
``width`` as its only argument and may use ``core.storage`` to persist state.
"""

import importlib.util
import inspect
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

EXTENSIONS_DIR = Path(__file__).resolve().parent.parent / "extensions"

_registry: dict[str, "Plugin"] = {}
_loaded_dirs: set[Path] = set()
_builtins_loaded = False


@dataclass(frozen=True)
class Plugin:
    name: str
    key: str
    description: str
    handler: Callable[[int], None]


def register(name, key, description=None):
    """Decorator that registers a callable as a Focus Hub plugin."""

    def decorator(func):
        if key in _registry:
            print(f"plugin key '{key}' is already taken, skipping '{name}'")
            return func
        _registry[key] = Plugin(
            name=name,
            key=key,
            description=description or inspect.getdoc(func) or func.__name__,
            handler=func,
        )
        return func

    return decorator


def reset():
    """Clear the registry and load caches. Mainly useful for tests."""
    global _builtins_loaded
    _registry.clear()
    _loaded_dirs.clear()
    _builtins_loaded = False


def load_builtins():
    """Register the core commands shipped with Focus Hub."""
    global _builtins_loaded
    if _builtins_loaded:
        return
    from core.pomodoro import pomodoro
    from core.todo import manage_tasks
    from core.storage import load
    from core.utils import in_dev

    register("⏱  pomodoro timer", "p", "Run a focused pomodoro session")(pomodoro)
    register("  to-do", "t", "Manage your task list")(
        lambda w: manage_tasks(load("todo.json"), w)
    )
    register("  import-data-to-.json", "j", "Export data to JSON")(in_dev)
    register(" import-data-to-Obsidian", "o", "Export data to Obsidian")(in_dev)
    register(" settings", "s", "Change Focus Hub settings")(in_dev)
    _builtins_loaded = True


def _import_extension(path):
    module_name = f"_focus_extension_{path.stem}"
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        return
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    try:
        spec.loader.exec_module(module)
    except Exception as exc:
        sys.modules.pop(module_name, None)
        print(f"[plugins] failed to load {path.name}: {exc}")


def load_plugins(extensions_dir=None):
    """Import every ``*.py`` module in an extensions directory."""
    directory = Path(extensions_dir or EXTENSIONS_DIR).resolve()
    if directory in _loaded_dirs or not directory.is_dir():
        return
    for path in sorted(directory.glob("*.py")):
        if path.name == "__init__.py":
            continue
        _import_extension(path)
    _loaded_dirs.add(directory)


def menu_items():
    """Return ``[(name, key), ...]`` in the order plugins were registered."""
    return [(p.name, p.key) for p in _registry.values()]


def get_plugin(key):
    return _registry.get(key)


def run(key, width):
    """Dispatch a menu key to its handler, catching plugin errors."""
    plugin = _registry.get(key)
    if plugin is None:
        print(f"command not found: {key}")
        return False
    try:
        plugin.handler(width)
    except Exception as exc:
        print(f"[{plugin.name}] error: {exc}")
        return False
    return True