"""Terminal screen, cursor and sizing helpers."""

import os
import sys


def clear_screen() -> None:
    sys.stdout.write("\x1b[2J\x1b[H")
    sys.stdout.flush()


def home_screen() -> None:
    """Move the cursor to the top-left without clearing (flicker-free redraw)."""
    sys.stdout.write("\x1b[H")
    sys.stdout.flush()


def hide_cursor() -> None:
    sys.stdout.write("\x1b[?25l")
    sys.stdout.flush()


def show_cursor() -> None:
    sys.stdout.write("\x1b[?25h")
    sys.stdout.flush()


def get_terminal_width() -> int:
    try:
        return os.get_terminal_size().columns
    except OSError:
        return 80


def get_terminal_height() -> int:
    try:
        return os.get_terminal_size().lines
    except OSError:
        return 24