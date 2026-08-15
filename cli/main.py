from core.utils import (
    clear_screen,
    get_terminal_width,
    in_dev,
    center_line,
    lerp_color,
    colorize,
)
from core.todo import manage_tasks
from core.pomodoro import pomodoro
from extensions.habbit_track import habbits_manage, habbit_tracker
from core.config import WELCOME_ART, ITEMS_MENU
import os
import time

todo_list = []
habbit_list = []

manager = {
    "t": (manage_tasks, todo_list),
    "p": (pomodoro,),
    "j": (in_dev,),
    "o": (in_dev,),
    "s": (in_dev,),
}


def main():
    while True:
        clear_screen()
        width = get_terminal_width()
        height = os.get_terminal_size().lines
        content_height = 5 + (len(ITEMS_MENU) * 2)
        top_padding = max(1, ((height - content_height) // 2) - 5)
        print("\n" * top_padding)
        art_lines = [l for l in WELCOME_ART.split("\n") if l.strip()]
        for i, line in enumerate(art_lines):
            t = i / max(1, len(art_lines) - 1)
            r, g, b = lerp_color("#4ea8ff", "#7f88ff", t)
            print(center_line(colorize(line, r, g, b), width))

        print("\n" * 2)

        n = len(ITEMS_MENU)
        for i, (name, key) in enumerate(ITEMS_MENU):
            row = f"{name:<70}{key:>5}"
            r, g, b = lerp_color("#4ea8ff", "#7f88ff", i / n if n else 0)
            print(
                center_line(colorize(row, r, g, b), width)
            )  # colorize make ANSI truecolor-code
            print()

        print("\n")

        manage_inp = input("enter a letter: ").strip()
        if manage_inp == "q":
            break
        action = manager.get(manage_inp)  # func in manager
        if action:
            func, *args = action
            func(*args, width)
            time.sleep(2)
        else:
            print("command not found!".center(width))
            time.sleep(2)
    print(WELCOME_ART)


if __name__ == "__main__":
    main()
