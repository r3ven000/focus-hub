"""Typed JSON-file storage backend.

The app and its plugins persist state through the :class:`Storage` protocol.
:class:`JsonStorage` is the default backend (JSON files under ``data/``).
Plugins or tests can install a different implementation with
:func:`set_storage` without touching any call site.

The module-level :func:`load` / :func:`save` helpers delegate to the active
backend, so existing code keeps working unchanged.
"""

from __future__ import annotations

import copy
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Protocol, runtime_checkable

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


@runtime_checkable
class Storage(Protocol):
    """Persistence contract used across the app and by plugins."""

    def load(self, filename: str, default: Any = None) -> Any:
        """Return the contents of ``filename`` or a deep copy of ``default``.

        Invalid, missing or wrongly-typed data must not corrupt the app:
        implementations are expected to degrade to ``default``.
        """
        ...

    def save(self, filename: str, data: Any) -> None:
        """Atomically persist ``data`` under ``filename``."""
        ...


class JsonStorage:
    """JSON-file backend rooted at ``data_dir`` (defaults to ``DATA_DIR``)."""

    data_dir: Path | None

    def __init__(self, data_dir: Path | None = None) -> None:
        self.data_dir = data_dir

    def _path(self, filename: str) -> Path:
        base = self.data_dir or DATA_DIR
        return base / filename

    def save(self, filename: str, data: Any) -> None:
        # Write to a temporary file first, then swap it in atomically, so a
        # crash mid-write can never leave a half-written/corrupt file behind.
        path = self._path(filename)
        path.parent.mkdir(exist_ok=True)
        tmp = path.with_suffix(path.suffix + ".tmp")
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)

    def _backup_corrupt(self, path: Path) -> Path:
        base = self.data_dir or DATA_DIR
        base.mkdir(exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        for i in range(1000):
            suffix = f".corrupt.{stamp}" + (f"-{i}" if i else "")
            backup = path.with_suffix(path.suffix + suffix)
            if not backup.exists():
                path.rename(backup)
                return backup
        raise OSError(f"cannot create a backup for {path.name}")

    def load(self, filename: str, default: Any = None) -> Any:
        path = self._path(filename)
        if default is None:
            default = []
        if not path.exists():
            return copy.deepcopy(default)
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, ValueError, OSError):
            data = None
        # Guard against the wrong shape (e.g. a dict where a list is expected):
        # move the file aside for inspection and fall back to the default, so a
        # bad file never crashes the app.
        if not isinstance(data, type(default)):
            backup = self._backup_corrupt(path)
            print(f"{filename} is corrupt, backup saved to {backup.name}")
            return copy.deepcopy(default)
        return data


#: Default backend shared by the module-level helpers and plugins.
storage: Storage = JsonStorage()


def get_storage() -> Storage:
    """Return the active storage backend."""
    return storage


def set_storage(new_storage: Storage) -> None:
    """Install a different storage backend (tests, plugins, ...)."""
    global storage
    storage = new_storage


def save(filename: str, data: Any) -> None:
    storage.save(filename, data)


def load(filename: str, default: Any = None) -> Any:
    return storage.load(filename, default)
