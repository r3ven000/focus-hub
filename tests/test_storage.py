import json

from core import storage
from core.storage import JsonStorage, get_storage, set_storage


def _write(dirpath, name, content):
    path = dirpath / name
    path.write_text(content, encoding="utf-8")
    return path


def test_save_round_trip(isolated_data_dir):
    storage.save("round.json", ["buy milk", "walk"])
    assert storage.load("round.json") == ["buy milk", "walk"]


def test_save_is_atomic_and_cleans_tmp(isolated_data_dir):
    storage.save("atom.json", ["x"])
    assert not (isolated_data_dir / "atom.json.tmp").exists()
    data = json.loads((isolated_data_dir / "atom.json").read_text(encoding="utf-8"))
    assert data == ["x"]


def test_load_missing_returns_default(isolated_data_dir):
    assert storage.load("missing.json", default=["d"]) == ["d"]
    assert not (isolated_data_dir / "missing.json").exists()


def test_load_missing_default_is_not_aliased(isolated_data_dir):
    first = storage.load("missing.json", default=["x"])
    second = storage.load("missing.json", default=["x"])
    first.append("y")
    assert first == ["x", "y"]
    assert second == ["x"]
    assert first is not second


def test_load_empty_file_returns_default_and_backs_up(isolated_data_dir):
    _write(isolated_data_dir, "empty.json", "")
    assert storage.load("empty.json") == []
    assert not (isolated_data_dir / "empty.json").exists()
    assert list(isolated_data_dir.glob("empty.json.corrupt*"))


def test_load_wrong_type_backs_up_and_returns_default(isolated_data_dir):
    _write(isolated_data_dir, "dict.json", '{"a": 1}')
    assert storage.load("dict.json") == []
    assert not (isolated_data_dir / "dict.json").exists()


def test_load_deeply_broken_json_backs_up(isolated_data_dir):
    _write(isolated_data_dir, "bad.json", "{bad")
    assert storage.load("bad.json") == []
    assert list(isolated_data_dir.glob("bad.json.corrupt*"))


def test_corrupt_backup_does_not_overwrite_previous(isolated_data_dir):
    _write(isolated_data_dir, "c.json", "{bad")
    _write(isolated_data_dir, "c.json.corrupt.20200101-000000", "OLD")
    storage.load("c.json")
    backups = sorted(p.name for p in isolated_data_dir.glob("c.json.corrupt*"))
    assert len(backups) == 2
    old = isolated_data_dir / "c.json.corrupt.20200101-000000"
    assert old.read_text(encoding="utf-8") == "OLD"


def test_load_dict_default_type(isolated_data_dir):
    _write(isolated_data_dir, "d.json", '{"k": 1}')
    assert storage.load("d.json", default={}) == {"k": 1}


def test_json_storage_custom_directory(tmp_path):
    custom = tmp_path / "custom"
    store = JsonStorage(custom)
    store.save("x.json", ["a", "b"])
    assert store.load("x.json") == ["a", "b"]
    assert (custom / "x.json").exists()
    assert not (tmp_path / "x.json").exists()


class InMemoryStorage:
    """A minimal Storage implementation used to prove backend swapping."""

    def __init__(self):
        self.data: dict = {}

    def load(self, filename: str, default=None):
        return self.data.get(filename, default)

    def save(self, filename: str, data) -> None:
        self.data[filename] = data


def test_set_storage_swaps_backend():
    original = get_storage()
    try:
        backend = InMemoryStorage()
        set_storage(backend)
        storage.save("mem.json", [1, 2])
        assert get_storage() is backend
        assert storage.load("mem.json") == [1, 2]
    finally:
        set_storage(original)


def test_storage_protocol_is_runtime_checkable():
    import inspect

    assert inspect.isclass(JsonStorage)
    assert isinstance(JsonStorage(), storage.Storage)