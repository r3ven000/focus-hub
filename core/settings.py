"""Persistent user settings: gradient colors and enabled extensions.

Settings live in ``data/settings.json`` and are applied at startup by
``apply_settings``, which mutates ``core.config`` so every screen picks the
change up immediately. However, extension loading happens only once at
startup, so toggling extensions is announced as "takes effect on restart".
"""

from __future__ import annotations

import re
import time
from typing import Any

from . import config
from .banner import print_banner, render_menu
from .color import colorize, lerp_color, tint_center
from .storage import load as storage_load
from .storage import save as storage_save
from .terminal import clear_screen, get_terminal_width

SETTINGS_FILENAME = "settings.json"

# Fallback defaults, used only when a color key is missing or invalid.
DEFAULT_SETTINGS: dict[str, Any] = {
    "gradient_start": config.GRADIENT_START,
    "gradient_end": config.GRADIENT_END,
}

# A color is exactly "#RRGGBB" (hex, case-insensitive).
_HEX_RE = re.compile(r"^#[0-9a-fA-F]{6}$")


def is_valid_hex(color: str) -> bool:
    """Return True if ``color`` is a well-formed ``#RRGGBB`` value."""
    return bool(_HEX_RE.match(color))


def load_settings(filename: str = SETTINGS_FILENAME) -> dict[str, Any]:
    """Load ``filename`` and fill in the default color values."""
    data = storage_load(filename, default={})
    merged: dict[str, Any] = DEFAULT_SETTINGS.copy()
    if isinstance(data, dict):
        merged.update(data)
    return merged


def save_settings(settings: dict[str, Any], filename: str = SETTINGS_FILENAME) -> None:
    """Persist the whole settings dict."""
    storage_save(filename, settings)


def apply_settings(settings: dict[str, Any]) -> None:
    """Push gradient colors from ``settings`` into ``core.config``.

    ``tint`` reads ``config.GRADIENT_START/END`` on every call, so the whole
    UI (menu, timers, managers) switches to the new palette immediately.
    Invalid values are ignored and the current color is kept.
    """
    start = settings.get("gradient_start", DEFAULT_SETTINGS["gradient_start"])
    if is_valid_hex(str(start)):
        config.GRADIENT_START = start
    end = settings.get("gradient_end", DEFAULT_SETTINGS["gradient_end"])
    if is_valid_hex(str(end)):
        config.GRADIENT_END = end


def enabled_extensions(filename: str = SETTINGS_FILENAME) -> list[str] | None:
    """Return the list of extension file stems allowed to load.

    ``None`` means "no filter, load everything" (the default when the key is
    absent). An empty list means nothing is loaded. A non-empty list means
    only those stems are imported.
    """
    data = load_settings(filename)
    value = data.get("enabled_extensions")
    if isinstance(value, list):
        return [str(item) for item in value if isinstance(item, str)]
    return None


def preview_gradient(start_hex: str, end_hex: str, width: int) -> str:
    """Render a solid gradient strip used as a live color preview."""
    n = max(1, width)
    return "".join(
        colorize("█", *lerp_color(start_hex, end_hex, i / max(1, n - 1)))
        for i in range(n)
    )


def _available_extensions() -> list[str]:
    """List discoverable extension file stems (lazy import, avoids a cycle)."""
    from .plugins import available_extensions as list_extensions

    return list_extensions()


_COMMAND_KEYS: dict[str, str] = {"1": "colors", "2": "extensions", "3": "quit"}
_COLOR_COMMAND_KEYS: dict[str, str] = {"1": "top", "2": "bottom", "3": "quit"}


class SettingsManager:
    """Interactive settings screen: colors and extension toggles."""

    def __init__(
        self, filename: str = SETTINGS_FILENAME, title: str = "settings"
    ) -> None:
        self.filename = filename
        self.title = title
        self.settings: dict[str, Any] = {}

    def run(self, width: int | None = None) -> None:
        self.settings = load_settings(self.filename)
        while True:
            clear_screen()
            width = get_terminal_width()
            self._show(width)

            raw = input(tint_center("1.colors 2.extensions 3.quit : ", width)).strip()
            parts: list[str] = raw.split()
            if not parts:
                continue
            command = _COMMAND_KEYS.get(parts[0].lower(), parts[0].lower())

            if command == "quit":
                break
            elif command == "colors":
                self._colors_menu(width)
            elif command == "extensions":
                self._extensions_menu(width)
            else:
                print(tint_center("unknown command", width))
                time.sleep(1)

    def _show(self, width: int) -> None:
        print_banner(self.title, width)
        print(tint_center("Change Focus Hub settings.", width, 0.0))
        print()
        for row in render_menu(self._command_rows(), width):
            print(row)

    def _command_rows(self) -> list[tuple[str, str]]:
        return [
            ("customize colors", "1"),
            ("extensions", "2"),
            ("quit", "3"),
        ]

    def _colors_menu(self, width: int) -> None:
        while True:
            clear_screen()
            width = get_terminal_width()
            self._show_colors(width)

            raw = input(tint_center("1.top 2.bottom 3.quit : ", width)).strip()
            parts: list[str] = raw.split()
            if not parts:
                continue
            command = _COLOR_COMMAND_KEYS.get(parts[0].lower(), parts[0].lower())

            if command == "quit":
                break
            elif command in ("top", "bottom"):
                self._set_color(parts, width, top=command == "top")
            else:
                print(tint_center("unknown command", width))
                time.sleep(1)

    def _show_colors(self, width: int) -> None:
        print_banner("colors", width)
        print(tint_center("Customize the gradient.", width, 0.0))
        print()

        # Show each color's hex code, tinted with its own color.
        top = str(
            self.settings.get("gradient_start", DEFAULT_SETTINGS["gradient_start"])
        )
        bottom = str(
            self.settings.get("gradient_end", DEFAULT_SETTINGS["gradient_end"])
        )
        print(tint_center(f"top color code    : {top}", width, 0.0))
        print(tint_center(f"bottom color code : {bottom}", width, 1.0))
        print()
        print(tint_center(preview_gradient(top, bottom, min(40, width)), width))
        print()
        for row in render_menu(self._color_command_rows(), width):
            print(row)

    def _color_command_rows(self) -> list[tuple[str, str]]:
        return [
            ("top <color>", "1"),
            ("bottom <color>", "2"),
            ("quit", "3"),
        ]

    def _set_color(self, parts: list[str], width: int, *, top: bool) -> None:
        key = "gradient_start" if top else "gradient_end"
        label = "top" if top else "bottom"
        color = parts[1] if len(parts) > 1 else ""
        if not color:
            color = input(
                tint_center(f"enter {label} color (#RRGGBB): ", width)
            ).strip()
        if not is_valid_hex(color):
            print(tint_center("invalid color, use #RRGGBB", width))
            time.sleep(1)
            return
        self.settings[key] = color
        apply_settings(self.settings)
        save_settings(self.settings, self.filename)
        print(tint_center(f"{label} color set to {color}", width))
        time.sleep(1)

    def _extensions_menu(self, width: int) -> None:
        while True:
            clear_screen()
            width = get_terminal_width()
            exts = _available_extensions()
            self._show_extensions(width, exts)

            raw = input(tint_center("toggle <index> | quit : ", width)).strip()
            if raw in ("quit", "q"):
                break
            try:
                idx = int(raw) - 1
            except ValueError:
                print(tint_center("unknown command", width))
                time.sleep(1)
                continue
            if not 0 <= idx < len(exts):
                print(tint_center("invalid index", width))
                time.sleep(1)
                continue
            self._toggle_extension(exts[idx], exts, width)

    def _show_extensions(self, width: int, exts: list[str]) -> None:
        print_banner("extensions", width)
        print(tint_center("Choose which extensions load at startup.", width, 0.0))
        print()
        enabled = self.settings.get("enabled_extensions")
        selection = enabled if isinstance(enabled, list) else exts
        n = max(1, len(exts))
        for i, ext in enumerate(exts, start=1):
            state = "on" if ext in selection else "off"
            tint_value = (i - 1) / max(1, n - 1)
            print(tint_center(f"{i}. {ext:<24} [{state}]", width, tint_value))
        if not exts:
            print(tint_center("no extensions found", width))
        print()
        print(tint_center("changes take effect on restart", width, 0.0))
        print("\n" * 2)

    def _toggle_extension(self, stem: str, exts: list[str], width: int) -> None:
        stored = self.settings.get("enabled_extensions")
        if stored is None:
            # All extensions are on by default.
            stored = list(exts)
        now_enabled = stem not in stored
        if now_enabled:
            stored.append(stem)
            stored.sort()
        else:
            stored.remove(stem)
        # If everything ends up enabled, normalise back to "all" (None).
        if stored and sorted(stored) == sorted(exts):
            self.settings.pop("enabled_extensions", None)
        else:
            self.settings["enabled_extensions"] = stored
        save_settings(self.settings, self.filename)
        state = "enabled" if now_enabled else "disabled"
        print(tint_center(f"{stem} is now {state}", width))
        time.sleep(1)


_SETTINGS_MANAGER: SettingsManager = SettingsManager()


def settings_menu(width: int) -> None:
    """Open the interactive settings screen (menu entry point)."""
    _SETTINGS_MANAGER.run(width)
