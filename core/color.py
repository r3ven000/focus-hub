"""ANSI color helpers and the brand gradient used across the UI."""

import re

from . import config

ANSI_RE = re.compile(r"\x1b\[[0-9;]*m", re.UNICODE)


def center_line(text: str, width: int) -> str:
    # ANSI codes are invisible to the terminal, so we strip them before
    # measuring the visible width; otherwise the centering would be off.
    visible = ANSI_RE.sub("", text).rstrip("\n")
    pad = max(0, (width - len(visible)) // 2)
    return " " * pad + text


def lerp_color(hex_start: str, hex_end: str, t: float) -> tuple[int, int, int]:
    # "lerp" = linear interpolation: blend each red/green/blue channel from
    # the start colour towards the end colour by the factor ``t`` (0..1).
    start = [int(hex_start[i : i + 2], 16) for i in (1, 3, 5)]
    end = [int(hex_end[i : i + 2], 16) for i in (1, 3, 5)]
    rgb = tuple(round(a + (b - a) * t) for a, b in zip(start, end))
    return (rgb[0], rgb[1], rgb[2])


def colorize(text: str, r: int, g: int, b: int) -> str:
    return f"\x1b[38;2;{r};{g};{b}m{text}\x1b[0m"


def tint(text: str, t: float = 0.5) -> str:
    """Color ``text`` with the brand gradient (same palette as the menu).

    Colors are read from ``config`` on every call, so settings that change
    ``config.GRADIENT_START/END`` take effect immediately across the UI.
    """
    r, g, b = lerp_color(
        config.GRADIENT_START, config.GRADIENT_END, max(0.0, min(1.0, t))
    )
    return colorize(text, r, g, b)


def tint_center(text: str, width: int, t: float = 0.5) -> str:
    """Center ``text`` in ``width`` columns and tint it with the brand palette."""
    return center_line(tint(text, t), width)
