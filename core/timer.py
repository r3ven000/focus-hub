"""Full-screen countdown timer with an ASCII clock and companion art."""

import sys
import time

from .banner import figlet
from .color import center_line, tint, tint_center
from .terminal import get_terminal_width, home_screen, hide_cursor, show_cursor


def timer(minutes: int | float, width: int, art: str) -> bool:
    end_time: float = time.time() + (minutes * 60)

    art_lines: list[str] = [line for line in art.split("\n") if line.strip()]
    max_art_len: int = max(len(line) for line in art_lines)

    hide_cursor()
    first: bool = True
    try:
        while time.time() < end_time:
            try:
                remaining: float = end_time - time.time()
                mins, secs = divmod(int(remaining), 60)

                # First frame wipes the whole screen; every later frame only
                # moves the cursor to the top-left and overwrites in place,
                # which avoids the visible flicker of a full clear.
                if first:
                    sys.stdout.write("\x1b[2J\x1b[H")
                    first = False
                else:
                    home_screen()
                sys.stdout.flush()
                width = get_terminal_width()
                pad: int = max(0, (width - max_art_len) // 2)
                print("\n" * 3)
                ascii_time = figlet.renderText(f"{mins:02d}:{secs:02d}")
                time_lines = [line for line in ascii_time.split("\n") if line.strip()]
                for i, line in enumerate(time_lines):
                    t = i / max(1, len(time_lines) - 1)
                    print(center_line(tint(line, t), width))
                for i, line in enumerate(art_lines):
                    t = i / max(1, len(art_lines) - 1)
                    print(" " * pad + tint(line, t))
                time.sleep(0.5)
            except KeyboardInterrupt:
                return False
        print(tint_center("time's up", width))
        time.sleep(1)
        return True
    finally:
        show_cursor()