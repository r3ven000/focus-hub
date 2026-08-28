import pytest

import core.timer as timer_module
from core.pomodoro import PomodoroManager


class FakeTime:
    def __init__(self):
        self.now = 0.0

    def time(self):
        return self.now

    def sleep(self, seconds):
        self.now += seconds


@pytest.fixture
def fake_time(monkeypatch):
    fake = FakeTime()
    monkeypatch.setattr(timer_module, "time", fake)
    return fake


def test_run_session_full_cycle(fake_time, capsys):
    manager = PomodoroManager(work_time=10, break_time=5)
    assert manager.run_session(80) is True
    out = capsys.readouterr().out
    assert "staeting session" in out
    assert "starting break" in out
    assert manager.cycles == 1


def test_run_session_interrupt_skips_break(monkeypatch, capsys):
    class InterruptingTime(FakeTime):
        def sleep(self, seconds):
            raise KeyboardInterrupt

    monkeypatch.setattr(timer_module, "time", InterruptingTime())
    manager = PomodoroManager()
    assert manager.run_session(80) is False
    out = capsys.readouterr().out
    assert "staeting session" in out
    assert "starting break" not in out
    assert manager.cycles == 0


def test_manager_run_with_commands(monkeypatch, capsys):
    fake = FakeTime()
    monkeypatch.setattr(timer_module, "time", fake)
    keys = iter(["start", "quit"])

    def fake_input(prompt=""):
        return next(keys)

    monkeypatch.setattr("builtins.input", fake_input)
    manager = PomodoroManager(work_time=1, break_time=1)
    manager.run(80)
    out = capsys.readouterr().out
    assert "Interactive pomodoro session manager." in out
    assert "staeting session" in out
    assert "starting break" in out
    assert manager.cycles == 1


def test_manager_unknown_command(monkeypatch, capsys):
    keys = iter(["zz", "quit"])

    def fake_input(prompt=""):
        return next(keys)

    monkeypatch.setattr("builtins.input", fake_input)
    manager = PomodoroManager(work_time=30, break_time=10)
    manager.run(80)
    assert "unknown command" in capsys.readouterr().out


def test_manager_ignores_empty_input(monkeypatch, capsys):
    keys = iter(["", "quit"])

    def fake_input(prompt=""):
        return next(keys)

    monkeypatch.setattr("builtins.input", fake_input)
    manager = PomodoroManager(work_time=30, break_time=10)
    manager.run(80)
    assert "Interactive pomodoro session manager." in capsys.readouterr().out


def test_manager_sets_durations_via_commands(monkeypatch, capsys):
    keys = iter(["work 30", "break 10", "quit"])

    def fake_input(prompt=""):
        return next(keys)

    monkeypatch.setattr("builtins.input", fake_input)
    manager = PomodoroManager(work_time=25, break_time=5)
    manager.run(80)
    assert manager.work_time == 30
    assert manager.break_time == 10


def test_manager_set_duration_without_value(capsys):
    manager = PomodoroManager()
    manager._set_duration(["work"], 80, work=True)
    out = capsys.readouterr().out
    assert "please provide minutes, e.g. work 25" in out
    assert manager.work_time == 25


def test_manager_set_duration_non_positive(capsys):
    manager = PomodoroManager()
    manager._set_duration(["break", "0"], 80, work=False)
    out = capsys.readouterr().out
    assert "duration must be positive" in out
    assert manager.break_time == 5


def test_manager_sets_duration_fields():
    manager = PomodoroManager(work_time=25, break_time=5)
    manager._set_duration(["work", "30"], 80, work=True)
    manager._set_duration(["break", "10"], 80, work=False)
    assert manager.work_time == 30
    assert manager.break_time == 10


def test_manager_rejects_invalid_duration(capsys):
    manager = PomodoroManager(work_time=25, break_time=5)
    manager._set_duration(["work", "abc"], 80, work=True)
    out = capsys.readouterr().out
    assert "please enter a valid number" in out
    assert manager.work_time == 25


def test_pomodoro_entry_point_runs_manager(monkeypatch, capsys):
    from core import pomodoro

    keys = iter(["quit"])

    def fake_input(prompt=""):
        return next(keys)

    monkeypatch.setattr("builtins.input", fake_input)
    pomodoro.pomodoro(80)
    assert "Interactive pomodoro session manager." in capsys.readouterr().out