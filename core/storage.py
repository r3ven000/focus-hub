import json
from pathlib import Path


def save(filename, data):
    path = Path("data")
    path.mkdir(exist_ok=True)
    with open(path / filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load(filename):
    path = Path("data") / filename
    if not path.exists():
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, ValueError):
        print(f"{filename} is corrupt, saving a backup copy")
        backup = path.with_suffix(
            path.suffix + ".corrupt"
        )  # todo.json → todo.json.corrupt
        path.rename(backup)
        return []
