import copy
import json
import os
from datetime import datetime
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def _path(filename):
    return DATA_DIR / filename


def save(filename, data):
    path = _path(filename)
    path.parent.mkdir(exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)


def _backup_corrupt(path):
    DATA_DIR.mkdir(exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    for i in range(1000):
        suffix = f".corrupt.{stamp}" + (f"-{i}" if i else "")
        backup = path.with_suffix(path.suffix + suffix)
        if not backup.exists():
            path.rename(backup)
            return backup
    raise OSError(f"cannot create a backup for {path.name}")


def load(filename, default=None):
    path = _path(filename)
    if default is None:
        default = []
    if not path.exists():
        return copy.deepcopy(default)
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, ValueError, OSError):
        data = None
    if not isinstance(data, type(default)):
        backup = _backup_corrupt(path)
        print(f"{filename} is corrupt, backup saved to {backup.name}")
        return copy.deepcopy(default)
    return data
