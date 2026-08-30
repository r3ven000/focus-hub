import pytest

import core.timer as timer_module
from core.timer import timer


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


def test_timer_runs_to_completion(fake_time, capsys):
    assert timer(0.01, 80, art="computer") is True
    assert "time's up" in capsys.readouterr().out


def test_timer_interrupt_returns_false(monkeypatch):
    class InterruptingTime(FakeTime):
        def sleep(self, seconds):
            raise KeyboardInterrupt

    monkeypatch.setattr(timer_module, "time", InterruptingTime())
    assert timer(25, 80, art="computer") is False


def test_timer_clears_once_then_redraws_in_place(fake_time, capsys):
    timer(0.01, 80, art="computer")
    out = capsys.readouterr().out
    assert out.count("\x1b[2J") == 1
    assert out.count("\x1b[H") > 1
    assert "\x1b[?25l" in out
    assert "\x1b[?25h" in out
