import pytest

from core import pomodoro, utils


class FakeTime:
    def __init__(self):
        self.now = 0.0

    def time(self):
        return self.now

    def sleep(self, seconds):
        self.now += seconds


class InterruptingTime(FakeTime):
    def sleep(self, seconds):
        raise KeyboardInterrupt


@pytest.fixture
def fake_time(monkeypatch):
    fake = FakeTime()
    monkeypatch.setattr(utils, "time", fake)
    return fake


@pytest.fixture
def fake_interrupt(monkeypatch):
    monkeypatch.setattr(utils, "time", InterruptingTime())


def test_timer_runs_to_completion(fake_time, capsys):
    result = utils.timer(0.01, 80, art="computer")
    assert result is True
    assert "time's up" in capsys.readouterr().out


def test_timer_interrupt_returns_false(fake_interrupt, capsys):
    result = utils.timer(25, 80, art="computer")
    assert result is False


def test_pomodoro_full_session(fake_time, monkeypatch, capsys):
    monkeypatch.setattr(pomodoro, "WORK_TIME", 0.01)
    monkeypatch.setattr(pomodoro, "BREAK_TIME", 0.01)
    pomodoro.pomodoro(80)
    out = capsys.readouterr().out
    assert "staeting session" in out
    assert "starting break" in out


def test_pomodoro_skips_break_on_interrupt(fake_interrupt, monkeypatch, capsys):
    pomodoro.pomodoro(80)
    out = capsys.readouterr().out
    assert "staeting session" in out
    assert "starting break" not in out