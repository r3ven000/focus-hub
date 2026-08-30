import datetime

import pytest

import core.habit_manager as habit_module
from core import plugins, storage
from extensions import habit_track


@pytest.fixture
def fixed_today(monkeypatch):
    day = datetime.date(2026, 8, 28)
    monkeypatch.setattr(habit_module, "_today", lambda: day)
    return day


def test_habit_add(isolated_data_dir, scripted_input):
    scripted_input(["add gym", "quit"])
    habit_track.habit_tracker()
    assert storage.load("habits.json", default={}) == {"gym": []}


def test_habit_add_rejects_empty(isolated_data_dir, scripted_input, capsys):
    scripted_input(["add", "quit"])
    habit_track.habit_tracker()
    out = capsys.readouterr().out
    assert "habit cannot be empty" in out
    assert storage.load("habits.json", default={}) == {}


def test_habit_add_rejects_duplicate(isolated_data_dir, scripted_input, capsys):
    storage.save("habits.json", {"gym": []})
    scripted_input(["add gym", "quit"])
    habit_track.habit_tracker()
    out = capsys.readouterr().out
    assert "habit already exists" in out
    assert storage.load("habits.json", default={}) == {"gym": []}


def test_habit_delete(isolated_data_dir, scripted_input):
    storage.save("habits.json", {"gym": [], "read": []})
    scripted_input(["del 1", "quit"])
    habit_track.habit_tracker()
    assert storage.load("habits.json", default={}) == {"read": []}


def test_habit_mark_done_today(isolated_data_dir, scripted_input, capsys, fixed_today):
    storage.save("habits.json", {"gym": []})
    scripted_input(["done 1", "quit"])
    habit_track.habit_tracker()
    assert storage.load("habits.json", default={}) == {"gym": [fixed_today.isoformat()]}
    assert "done" in capsys.readouterr().out


def test_habit_mark_done_on_date(
    isolated_data_dir, scripted_input, capsys, fixed_today
):
    storage.save("habits.json", {"gym": ["2026-08-20"]})
    scripted_input(["done 1 2026-08-25", "quit"])
    habit_track.habit_tracker()
    assert storage.load("habits.json", default={}) == {
        "gym": ["2026-08-20", "2026-08-25"]
    }


def test_habit_undone(
    isolated_data_dir, scripted_input, capsys, fixed_today
):
    storage.save("habits.json", {"gym": ["2026-08-25"]})
    scripted_input(["undone 1 2026-08-25", "quit"])
    habit_track.habit_tracker()
    assert storage.load("habits.json", default={}) == {"gym": []}


def test_habit_rejects_bad_dates(
    isolated_data_dir, scripted_input, capsys, fixed_today
):
    storage.save("habits.json", {"gym": []})
    scripted_input(
        [
            "done 1 not-a-date",
            "done 1 2026-08-29",
            "quit",
        ]
    )
    habit_track.habit_tracker()
    out = capsys.readouterr().out
    assert "invalid date, use YYYY-MM-DD" in out
    assert "cannot mark a future date" in out
    assert storage.load("habits.json", default={}) == {"gym": []}


def test_habit_grid_renders_squares(
    isolated_data_dir, scripted_input, capsys, fixed_today
):
    storage.save(
        "habits.json",
        {
            "gym": ["2026-08-28", "2026-08-27", "2026-08-26"],
        },
    )
    scripted_input(["grid 1", "", "quit"])
    habit_track.habit_tracker()
    out = capsys.readouterr().out
    assert "▪" in out
    assert "\x1b[38;2;" in out
    assert "streak 3" in out


def test_habit_grid_for_all(scripted_input, capsys, fixed_today, isolated_data_dir):
    storage.save("habits.json", {"gym": ["2026-08-25"], "read": ["2026-08-24"]})
    scripted_input(["grid", "", "quit"])
    habit_track.habit_tracker()
    out = capsys.readouterr().out
    assert "gym: streak" in out
    assert "read: streak" in out
    assert "▪" in out


def test_habit_validation(isolated_data_dir, scripted_input, capsys):
    storage.save("habits.json", {"gym": []})
    scripted_input(
        [
            "del 9",
            "done",
            "del abc",
            "undone",
            "undone 9",
            "undone 1 not-a-date",
            "grid 9",
            "bogus",
            "quit",
        ]
    )
    habit_track.habit_tracker()
    out = capsys.readouterr().out
    assert "invalid index" in out
    assert "index not found, try again" in out
    assert "please enter a valid number" in out
    assert "unknown command" in out
    assert "invalid date, use YYYY-MM-DD" in out
    assert storage.load("habits.json", default={}) == {"gym": []}


def test_habit_wrong_typed_data_degrades_to_empty(
    isolated_data_dir, scripted_input, capsys
):
    storage.save("habits.json", ["gym", "read"])
    scripted_input(["quit"])
    habit_track.habit_tracker()
    out = capsys.readouterr().out
    assert "is corrupt" in out
    assert storage.load("habits.json", default={}) == {}


def test_habit_coerces_malformed_values(isolated_data_dir):
    storage.save("habits.json", {"gym": "abc", "read": [1, "2026-08-01", None]})
    assert habit_module.load_habits("habits.json") == {
        "gym": [],
        "read": ["2026-08-01"],
    }


def test_streak_counts_consecutive_days(monkeypatch):
    day = datetime.date(2026, 8, 28)
    monkeypatch.setattr(habit_module, "_today", lambda: day)
    manager = habit_module.HabitManager("habits.json")
    assert manager._streak(["2026-08-28", "2026-08-27", "2026-08-26"]) == 3
    assert manager._streak(["2026-08-27", "2026-08-26"]) == 2
    assert manager._streak(["2026-08-20"]) == 0
    assert manager._streak([]) == 0


def test_habit_is_a_registered_plugin():
    plugins.load_plugins()
    plugin = plugins.get_plugin("h")
    assert plugin is not None
    assert plugin.name == " habit tracker"
    assert plugin.description == "Track and review your habits"


def test_habit_empty_input_and_invalid_indexes(
    isolated_data_dir, scripted_input, capsys
):
    storage.save("habits.json", {"gym": []})
    scripted_input(["", "done 9", "grid nope", "", "quit"])
    habit_track.habit_tracker()
    out = capsys.readouterr().out
    assert "invalid index" in out
    assert "please enter a valid number" in out
    assert storage.load("habits.json", default={}) == {"gym": []}
