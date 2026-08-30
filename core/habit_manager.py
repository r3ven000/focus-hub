"""Habit tracker: per-day completion history with GitHub-style heatmaps.

Data is stored as ``{"habit": ["YYYY-MM-DD", ...], ...}``. A date appears in
the list once per day the habit was completed. An old flat-list format
(``["gym", "read"]``) is transparently migrated on load.
"""

from __future__ import annotations

import datetime
import time

from .banner import print_banner, render_menu
from .color import colorize, tint, tint_center
from .storage import load, save
from .terminal import clear_screen, get_terminal_width

_COMMAND_KEYS: dict[str, str] = {
    "1": "add",
    "2": "done",
    "3": "undone",
    "4": "grid",
    "5": "del",
    "6": "quit",
}

GREEN_LEVELS: list[tuple[int, int, int]] = [
    (34, 39, 46),
    (155, 233, 168),
    (64, 196, 99),
    (48, 161, 78),
    (33, 110, 57),
]
MONTH_CODES: list[str] = [
    "Ja", "Fe", "Mr", "Ap", "My", "Jn",
    "Jl", "Au", "Se", "Oc", "No", "De",
]
DAY_LABELS: list[str] = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
WEEKS: int = 26


def _today() -> datetime.date:
    return datetime.date.today()


def _today_iso() -> str:
    return _today().isoformat()


def _coerce_habits(data: object) -> dict[str, list[str]]:
    habits: dict[str, list[str]] = {}
    if isinstance(data, dict):
        for name, dates in data.items():
            if isinstance(name, str):
                if isinstance(dates, list):
                    habits[name] = [str(d) for d in dates if isinstance(d, str)]
                else:
                    habits[name] = []
    return habits


def load_habits(filename: str) -> dict[str, list[str]]:
    # ``load`` already type-checks (expects a dict here); ``_coerce_habits``
    # strips any non-string junk inside, so we always get clean data.
    return _coerce_habits(load(filename, default={}))


class HabitManager:
    """Manage habits and their per-day completion history."""

    def __init__(
        self,
        filename: str,
        *,
        label: str = "habit",
        title: str = "habits",
    ) -> None:
        self.filename = filename
        self.label = label
        self.title = title

    def run(self, width: int | None = None) -> None:
        habits = load_habits(self.filename)
        while True:
            clear_screen()
            width = get_terminal_width()
            self._show_list(habits, width)

            raw = input(
                tint_center("1.add 2.done 3.undone 4.grid 5.del 6.quit : ", width)
            ).strip()
            parts: list[str] = raw.split()
            if not parts:
                continue
            command = _COMMAND_KEYS.get(parts[0].lower(), parts[0].lower())

            if command == "quit":
                break
            elif command == "add":
                self._add(habits, parts, width)
            elif command == "del":
                self._del(habits, parts, width)
            elif command == "done":
                self._done(habits, parts, width)
            elif command == "undone":
                self._undone(habits, parts, width)
            elif command == "grid":
                self._grid(habits, parts, width)
            else:
                print(tint_center("unknown command", width))
                time.sleep(1)

    def _show_list(self, habits: dict[str, list[str]], width: int) -> None:
        names = list(habits)
        print_banner(self.title, width)
        print(
            tint_center(
                "Per-day completion history with GitHub heatmaps.", width, 0.0
            )
        )
        print()
        for row in render_menu(self._command_rows(), width):
            print(row)
        print()

        n = max(1, len(names))
        for i, name in enumerate(names):
            dates = habits[name]
            today = _today_iso()
            mark = "done today" if today in dates else "-"
            row = (
                f"{i + 1}. {name:<18} streak={self._streak(dates):>2}"
                f"  total={len(set(dates)):>2}  {mark}"
            )
            print(tint_center(row, width, i / max(1, n - 1)))
        if not names:
            print(tint_center("there are no habits yet", width))
            print(tint("=" * width, 0.0) + "\n")

        print("\n\n\n")

    def _command_rows(self) -> list[tuple[str, str]]:
        return [
            ("add <name>", "1"),
            ("done <index> [date]", "2"),
            ("undone <index> [date]", "3"),
            ("grid [index]", "4"),
            (f"del <{self.label} index>", "5"),
            ("quit", "6"),
        ]

    def _add(self, habits: dict[str, list[str]], parts: list[str], width: int) -> None:
        name = " ".join(parts[1:]).strip()
        if not name:
            print(tint_center(f"{self.label} cannot be empty", width))
            time.sleep(1)
            return
        if name in habits:
            print(tint_center("habit already exists", width))
            time.sleep(1)
            return
        habits[name] = []
        save(self.filename, habits)

    def _del(self, habits: dict[str, list[str]], parts: list[str], width: int) -> None:
        names = list(habits)
        idx = self._parse_index(parts, width)
        if idx is None:
            return
        if not self._valid_index(idx, len(names), width):
            return
        del habits[names[idx]]
        save(self.filename, habits)

    def _done(self, habits: dict[str, list[str]], parts: list[str], width: int) -> None:
        names = list(habits)
        idx = self._parse_index(parts, width)
        if idx is None:
            return
        if not self._valid_index(idx, len(names), width):
            return
        name = names[idx]
        day = self._parse_user_date(parts, width)
        if day is None:
            return
        dates = habits[name]
        mark = day.isoformat()
        if mark not in dates:
            dates.append(mark)
            dates.sort()
            save(self.filename, habits)
        print(colorize(f"{name} done {mark}", *GREEN_LEVELS[3]))
        time.sleep(1)

    def _undone(
        self, habits: dict[str, list[str]], parts: list[str], width: int
    ) -> None:
        names = list(habits)
        idx = self._parse_index(parts, width)
        if idx is None:
            return
        if not self._valid_index(idx, len(names), width):
            return
        name = names[idx]
        day = self._parse_user_date(parts, width)
        if day is None:
            return
        dates = habits[name]
        mark = day.isoformat()
        if mark in dates:
            dates.remove(mark)
            save(self.filename, habits)
        print(tint_center(f"removed {name} from {mark}", width))
        time.sleep(1)

    def _parse_user_date(self, parts: list[str], width: int) -> datetime.date | None:
        text = parts[2] if len(parts) > 2 else _today_iso()
        try:
            day = datetime.date.fromisoformat(text)
        except ValueError:
            print(tint_center("invalid date, use YYYY-MM-DD", width))
            time.sleep(1)
            return None
        if day > _today():
            print(tint_center("cannot mark a future date", width))
            time.sleep(1)
            return None
        return day

    def _grid(
        self, habits: dict[str, list[str]], parts: list[str], width: int
    ) -> None:
        names = list(habits)
        if len(parts) > 1:
            idx = self._parse_index(parts, width)
            if idx is None:
                return
            if not self._valid_index(idx, len(names), width):
                return
            names = [names[idx]]
        for name in names:
            self._render_grid(name, habits[name], width)
        input(tint_center("press enter to continue...", width))

    def _render_grid(self, name: str, dates: list[str], width: int) -> None:
        today = _today()
        done = set(dates)
        week_start = today - datetime.timedelta(days=today.weekday())
        mondays = [
            week_start - datetime.timedelta(weeks=WEEKS - 1 - c)
            for c in range(WEEKS)
        ]
        # Build 7 (days) x WEEKS (columns) grid of intensity levels.
        # Level 0 = no completion; 1..4 = how strongly the day is "filled".
        columns: list[list[int]] = []
        for monday in mondays:
            column: list[int] = []
            for day_offset in range(7):
                day = monday + datetime.timedelta(days=day_offset)
                level = 0
                if day <= today and day.isoformat() in done:
                    level = min(4, dates.count(day.isoformat()))
                column.append(level)
            columns.append(column)

        print()
        print_banner(name, width)
        print(
            tint_center(
                f"{name}: streak {self._streak(dates)}"
                f" | total {len(done)} days",
                width,
            )
        )
        month_row = "   "
        for c, monday in enumerate(mondays):
            changed = c == 0 or monday.month != mondays[c - 1].month
            month_row += MONTH_CODES[monday.month - 1] if changed else "  "
        print(month_row)
        for day_offset in range(7):
            line = DAY_LABELS[day_offset] + " "
            for column in columns:
                line += colorize("▪ ", *GREEN_LEVELS[column[day_offset]])
            print(line)
        print(
            "   "
            + "".join(colorize("▪ ", *rgb) for rgb in GREEN_LEVELS)
            + "less -> more"
        )
        print(f"   today: {today.isoformat()}")

    def _streak(self, dates: list[str]) -> int:
        # Count consecutive done days running up to today (or up to yesterday
        # if today is not done yet), stopping at the first missing day.
        done = set(dates)
        today = _today()
        anchor = (
            today
            if today.isoformat() in done
            else today - datetime.timedelta(days=1)
        )
        count = 0
        day = anchor
        while day.isoformat() in done:
            count += 1
            day -= datetime.timedelta(days=1)
        return count

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

    def _valid_index(self, idx: int, size: int, width: int) -> bool:
        if not 0 <= idx < size:
            print(tint_center("invalid index", width))
            time.sleep(1)
            return False
        return True
