import io
import os

from core.utils import (
    center_line,
    clear_screen,
    colorize,
    in_dev,
    lerp_color,
    get_terminal_width,
)


def test_center_line_strips_ansi_when_padding():
    colored = colorize("hi", 1, 2, 3)
    line = center_line(colored, 10)
    assert line.startswith("    ")
    assert line.endswith("hi\x1b[0m")


def test_center_line_with_plain_text():
    assert center_line("abcd", 10) == "   abcd"


def test_lerp_color_endpoints():
    assert lerp_color("#000000", "#ffffff", 0.0) == (0, 0, 0)
    assert lerp_color("#000000", "#ffffff", 1.0) == (255, 255, 255)


def test_lerp_color_midpoint():
    assert lerp_color("#ff0000", "#0000ff", 0.5) == (128, 0, 128)


def test_in_dev_prints_notice(capsys):
    in_dev(80)
    assert "function in dev!" in capsys.readouterr().out


def test_clear_screen_writes_escape_sequence(capsys):
    clear_screen()
    assert "\x1b[2J" in capsys.readouterr().out


def test_get_terminal_width_falls_back_on_oserror(monkeypatch):
    def boom():
        raise OSError

    monkeypatch.setattr(os, "get_terminal_size", boom)
    assert get_terminal_width() == 80