from core import storage
from core.list_manager import GenericListManager


def test_command_rows_are_numbered():
    manager = GenericListManager("x.json", "task", heading="Custom heading")
    assert manager._command_rows() == [
        ("add", "1"),
        ("del <task index>", "2"),
        ("edit <task index>", "3"),
        ("quit", "4"),
    ]


def test_defaults_derive_from_label():
    manager = GenericListManager("x.json", "habit")
    assert manager.title == "HABITS"
    assert manager.empty == "there are no habits yet"
    assert manager.prompt == "1.add 2.del 3.edit 4.quit : "


def test_run_accepts_numeric_commands(isolated_data_dir, scripted_input):
    storage.save("list.json", ["keep", "drop"])
    manager = GenericListManager("list.json", "item")
    scripted_input(["2 2", "1 added", "quit"])
    result = manager.run()
    assert result == ["keep", "added"]
    assert storage.load("list.json") == ["keep", "added"]


def test_run_loads_from_disk_and_persists(isolated_data_dir, scripted_input):
    storage.save("list.json", [])
    manager = GenericListManager("list.json", "item")
    scripted_input(["add", "first", "add", "second", "del 1", "quit"])
    result = manager.run()
    assert result == ["second"]
    assert storage.load("list.json") == ["second"]


def test_run_list_mutates_in_place(isolated_data_dir, scripted_input):
    manager = GenericListManager("list.json", "item")
    items = ["keep"]
    scripted_input(["edit 1", "changed", "quit"])
    manager.run_list(items)
    assert items == ["changed"]
    assert storage.load("list.json") == ["changed"]