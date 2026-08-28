"""Generic interactive list editor shared by To-Do and habit tracking."""

from __future__ import annotations

import time

from .banner import print_banner, render_menu
from .color import tint, tint_center
from .storage import load, save
from .terminal import clear_screen, get_terminal_width

# Map numeric selections (1..4) to command names, mirroring the menu's
# letter keys but with indices. Both "del 3" and "2 3" work.
_COMMAND_KEYS: dict[str, str] = {"1": "add", "2": "del", "3": "edit", "4": "quit"}


class GenericListManager:
    """Interactive editor for a persisted list of strings.

    Displays a menu-style screen (ASCII-art banner + numbered command rows,
    like the main menu) and handles the ``add / del <index> / edit <index> /
    quit`` loop. Commands can be picked by their number (``1 gym``, ``2 3``)
    or by name (``add gym``, ``del 3``). The list is kept in sync with
    ``filename`` on every change.

    The ``label`` singular is used to build prompts and messages (``task``,
    ``habit``, ...); ``title`` names the banner shown at the top of the screen.
    """

    filename: str
    label: str
    title: str
    heading: str | None
    empty: str
    prompt: str

    def __init__(
        self,
        filename: str,
        label: str,
        *,
        title: str | None = None,
        heading: str | None = None,
        empty: str | None = None,
        prompt: str | None = None,
    ) -> None:
        self.filename = filename
        self.label = label
        self.title = title or (label.upper() + "S")
        self.heading = heading
        self.empty = empty or f"there are no {label}s yet"
        self.prompt = prompt or "1.add 2.del 3.edit 4.quit : "

    def run(self, width: int | None = None) -> list[str]:
        """Load the list from disk, run the editor and return the result."""
        items = load(self.filename)
        return self.run_list(items, width)

    def run_list(self, items: list[str], width: int | None = None) -> list[str]:
        """Run the editor against an already materialised ``items`` list."""
        while True:
            clear_screen()
            width = get_terminal_width()
            self._show(width)

            n = len(items)
            for index, item in enumerate(items, start=1):
                t = (index - 1) / max(1, n - 1) if n > 1 else 0.5
                print(tint_center(f"{index}. {item}", width, t))
            if not items:
                print(tint_center(self.empty, width))
                print(tint("=" * width, 0.0) + "\n")

            print("\n\n\n")

            raw = input(tint_center(self.prompt, width)).strip()
            parts: list[str] = raw.split()
            if not parts:
                continue
            # Accept a number (e.g. "1 gym") or the command name ("add gym").
            command = _COMMAND_KEYS.get(parts[0].lower(), parts[0].lower())

            if command == "quit":
                break
            elif command == "add":
                self._add(items, parts, width)
            elif command == "del":
                self._del(items, parts, width)
            elif command == "edit":
                self._edit(items, parts, width)
            else:
                print(tint_center("unknown command", width))
                time.sleep(1)
        return items

    def _show(self, width: int) -> None:
        print_banner(self.title, width)
        if self.heading:
            print(tint_center(self.heading, width, 0.0))
        print()
        for row in render_menu(self._command_rows(), width):
            print(row)

    def _command_rows(self) -> list[tuple[str, str]]:
        return [
            ("add", "1"),
            (f"del <{self.label} index>", "2"),
            (f"edit <{self.label} index>", "3"),
            ("quit", "4"),
        ]

    def _add(self, items: list[str], parts: list[str], width: int) -> None:
        new_item = " ".join(parts[1:]).strip()
        if not new_item:
            new_item = input(tint_center(f"enter {self.label}: ", width)).strip()
        if not new_item:
            print(tint_center(f"{self.label} cannot be empty", width))
            time.sleep(1)
            return
        items.append(new_item)
        save(self.filename, items)

    def _del(self, items: list[str], parts: list[str], width: int) -> None:
        idx = self._parse_index(parts, width)
        if idx is None:
            return
        if not self._valid_index(idx, items, width):
            return
        items.pop(idx)
        save(self.filename, items)

    def _edit(self, items: list[str], parts: list[str], width: int) -> None:
        idx = self._parse_index(parts, width)
        if idx is None:
            return
        if not self._valid_index(idx, items, width):
            return
        new_text = input(tint_center(f"enter new text {self.label}: ", width)).strip()
        if not new_text:
            print(tint_center(f"{self.label} cannot be empty", width))
            time.sleep(1)
            return
        items[idx] = new_text
        save(self.filename, items)

    def _parse_index(self, parts: list[str], width: int) -> int | None:
        if len(parts) <= 1:
            print(tint_center("index not found, try again", width))
            time.sleep(1)
            return None
        try:
            return int(parts[1]) - 1
        except ValueError:
            print(tint_center("please enter a valid number", width))
            time.sleep(1)
            return None

    def _valid_index(self, idx: int, items: list[str], width: int) -> bool:
        if not 0 <= idx < len(items):
            print(tint_center("invalid index", width))
            time.sleep(1)
            return False
        return True