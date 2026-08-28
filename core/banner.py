"""ASCII-art banners and main-menu-style rows, rendered with the brand gradient."""

from __future__ import annotations

from pyfiglet import Figlet

from .color import tint_center
from .terminal import get_terminal_width

figlet: Figlet = Figlet(font="roman")


def banner(text: str, width: int | None = None) -> list[str]:
    """Return gradient-tinted ASCII-art lines for ``text`` centered to ``width``."""
    if width is None:
        width = get_terminal_width()
    lines = [line for line in figlet.renderText(text).split("\n") if line.strip()]
    return [
        tint_center(line, width, i / max(1, len(lines) - 1))
        for i, line in enumerate(lines)
    ]


def print_banner(text: str, width: int | None = None) -> None:
    for line in banner(text, width):
        print(line)


def render_menu(rows: list[tuple[str, str]], width: int | None = None) -> list[str]:
    """Render ``(name, key)`` rows the same way the main menu does."""
    if width is None:
        width = get_terminal_width()
    n = max(1, len(rows))
    return [
        tint_center(f"{name:<70}{key:>5}", width, i / max(1, n - 1))
        for i, (name, key) in enumerate(rows)
    ]