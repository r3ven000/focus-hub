"""Interactive pomodoro session manager."""

from __future__ import annotations

import time

from .arts import coffee, computer
from .banner import print_banner, render_menu
from .color import tint_center
from .config import BREAK_TIME, WORK_TIME
from .terminal import clear_screen, get_terminal_width
from .timer import timer

_COMMAND_KEYS: dict[str, str] = {"1": "start", "2": "work", "3": "break", "4": "quit"}


class PomodoroManager:
    """Tune work/break durations and run pomodoro cycles from a small menu."""

    def __init__(
        self,
        work_time: int = WORK_TIME,
        break_time: int = BREAK_TIME,
        title: str = "pomodoro",
    ) -> None:
        self.work_time = work_time
        self.break_time = break_time
        self.title = title
        self.cycles = 0

    def run(self, width: int | None = None) -> None:
        """Open the interactive control screen."""
        while True:
            clear_screen()
            width = get_terminal_width()
            self._show_status(width)

            raw = input(
                tint_center("1.start 2.work 3.break 4.quit : ", width)
            ).strip()
            parts: list[str] = raw.split()
            if not parts:
                continue
            command = _COMMAND_KEYS.get(parts[0].lower(), parts[0].lower())

            if command == "quit":
                break
            elif command == "start":
                self.run_session(width)
            elif command == "work":
                self._set_duration(parts, width, work=True)
            elif command == "break":
                self._set_duration(parts, width, work=False)
            else:
                print(tint_center("unknown command", width))
                time.sleep(1)

    def run_session(self, width: int) -> bool:
        """Run one full work+break cycle. Returns False if it is interrupted."""
        # Work timer interrupted (Ctrl+C) -> don't start the break at all.
        print(tint_center("staeting session...", width))
        if not timer(self.work_time, width, art=computer):
            return False
        print(tint_center("starting break...", width))
        timer(self.break_time, width, art=coffee)
        self.cycles += 1
        return True

    def _set_duration(self, parts: list[str], width: int, *, work: bool) -> None:
        if len(parts) < 2:
            print(tint_center("please provide minutes, e.g. work 25", width))
            time.sleep(1)
            return
        try:
            minutes = int(parts[1])
        except ValueError:
            print(tint_center("please enter a valid number", width))
            time.sleep(1)
            return
        if minutes <= 0:
            print(tint_center("duration must be positive", width))
            time.sleep(1)
            return
        if work:
            self.work_time = minutes
        else:
            self.break_time = minutes

    def _show_status(self, width: int) -> None:
        print_banner(self.title, width)
        print(tint_center("Interactive pomodoro session manager.", width, 0.0))
        print()
        for row in render_menu(self._command_rows(), width):
            print(row)
        print()
        print(tint_center(f"completed cycles : {self.cycles}", width))
        print(tint_center(f"work time  : {self.work_time} min", width))
        print(tint_center(f"break time : {self.break_time} min", width))

    def _command_rows(self) -> list[tuple[str, str]]:
        return [
            ("start", "1"),
            ("work <minutes>", "2"),
            ("break <minutes>", "3"),
            ("quit", "4"),
        ]


_POMODORO_MANAGER: PomodoroManager = PomodoroManager()


def pomodoro(width: int) -> None:
    """Open the interactive pomodoro manager (menu entry point)."""
    _POMODORO_MANAGER.run(width)