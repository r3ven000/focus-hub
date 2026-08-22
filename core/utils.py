import os
import re
import time
from pyfiglet import Figlet
import sys
from core.arts import computer

figlet = Figlet(font="roman")


def clear_screen() -> None:
    sys.stdout.write("\x1b[2J\x1b[H")
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


def in_dev(*args):
    width = get_terminal_width()
    print("function in dev!".center(width))


def timer(minutes, width):
    end_time = time.time() + (minutes * 60)

    art_lines = [line for line in computer.split("\n") if line.strip()]
    max_art_len = max(len(line) for line in art_lines)

    while time.time() < end_time:
        try:
            remaining = end_time - time.time()
            mins, secs = divmod(int(remaining), 60)

            sys.stdout.write("\x1b[2J\x1b[H")
            sys.stdout.flush()
            width = get_terminal_width()
            pad = max(0, (width - max_art_len) // 2)
            print("\n" * 3)
            ascii_time = figlet.renderText(f"{mins:02d}:{secs:02d}")
            for line in ascii_time.split("\n"):
                if line.strip():
                    print(line.center(width))
            for line in art_lines:
                print(" " * pad + line)
            time.sleep(0.5)
        except KeyboardInterrupt:
            break
    print("time's up".center(width))
    time.sleep(1)


ANSI_RE = re.compile(r"\x1b\[[0-9;]*m", re.UNICODE)


def center_line(text: str, width: int) -> str:
    visible = ANSI_RE.sub("", text).rstrip("\n")
    pad = max(0, (width - len(visible)) // 2)
    return " " * pad + text


def lerp_color(hex_start, hex_end, t):
    start = [int(hex_start[i : i + 2], 16) for i in (1, 3, 5)]
    end = [int(hex_end[i : i + 2], 16) for i in (1, 3, 5)]
    rgb = tuple(round(a + (b - a) * t) for a, b in zip(start, end))
    return rgb


def colorize(text, r, g, b):
    return f"\x1b[38;2;{r};{g};{b}m{text}\x1b[0m"
