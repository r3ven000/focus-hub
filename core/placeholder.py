"""Placeholder features that are planned but not implemented yet."""

from typing import Any

from .color import tint_center
from .terminal import get_terminal_width


def in_dev(*args: Any) -> None:
    width = get_terminal_width()
    print(tint_center("function in dev!", width))
