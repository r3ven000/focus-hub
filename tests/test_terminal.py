import os

from core.terminal import (
    clear_screen,
    get_terminal_width,
    hide_cursor,
    home_screen,
    show_cursor,
)


def test_clear_screen_writes_escape_sequence(capsys):
    clear_screen()
    assert "\x1b[2J" in capsys.readouterr().out


def test_home_screen_moves_cursor_without_clearing(capsys):
    home_screen()
    out = capsys.readouterr().out
    assert "\x1b[H" in out
    assert "\x1b[2J" not in out


def test_cursor_hide_show_escape_sequences(capsys):
    hide_cursor()
    show_cursor()
    out = capsys.readouterr().out
    assert "\x1b[?25l" in out
    assert "\x1b[?25h" in out


def test_get_terminal_width_falls_back_on_oserror(monkeypatch):
    def boom():
        raise OSError

    monkeypatch.setattr(os, "get_terminal_size", boom)
    assert get_terminal_width() == 80
