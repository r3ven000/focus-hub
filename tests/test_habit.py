from extensions import habit_track
from core import plugins, storage


def test_habit_add(isolated_data_dir, scripted_input):
    scripted_input(["add", "gym", "quit"])
    habit_track.habit_tracker()
    assert storage.load("habits.json") == ["gym"]


def test_habit_edit_valid(isolated_data_dir, scripted_input):
    storage.save("habits.json", ["gym"])
    scripted_input(["edit 1", "yoga", "quit"])
    habit_track.habit_tracker()
    assert storage.load("habits.json") == ["yoga"]


def test_habit_delete_valid(isolated_data_dir, scripted_input):
    storage.save("habits.json", ["gym", "read"])
    scripted_input(["del 2", "quit"])
    habit_track.habit_tracker()
    assert storage.load("habits.json") == ["gym"]


def test_habit_validation(isolated_data_dir, scripted_input, capsys):
    storage.save("habits.json", ["only"])
    scripted_input(
        [
            "edit 9", "x",
            "del abc",
            "del 0",
            "add", "",
            "edit 1", "",
            "bogus",
            "quit",
        ]
    )
    habit_track.habit_tracker()
    out = capsys.readouterr().out
    assert "invalid index" in out
    assert "please enter a valid number" in out
    assert "habit cannot be empty" in out
    assert "unknown command" in out
    assert storage.load("habits.json") == ["only"]


def test_habit_is_a_registered_plugin():
    plugins.load_plugins()
    plugin = plugins.get_plugin("h")
    assert plugin is not None
    assert plugin.name == " habit tracker"
    assert plugin.description == "Track and review your habits"