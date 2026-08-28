from core.utils import (
    clear_screen,
    get_terminal_width,
    get_terminal_height,
    center_line,
    lerp_color,
    colorize,
)
from core.plugins import load_builtins, load_plugins, menu_items, run
from core.config import WELCOME_ART
import time


def main():
    load_builtins()
    load_plugins()
    while True:
        clear_screen()
        width = get_terminal_width()
        height = get_terminal_height()
        items = menu_items() + [(" quit", "q")]
        content_height = 5 + (len(items) * 2)
        top_padding = max(1, ((height - content_height) // 2) - 5)
        print("\n" * top_padding)
        art_lines = [line for line in WELCOME_ART.split("\n") if line.strip()]
        for i, line in enumerate(art_lines):
            t = i / max(1, len(art_lines) - 1)
            r, g, b = lerp_color("#4ea8ff", "#7f88ff", t)
            print(center_line(colorize(line, r, g, b), width))

        print("\n" * 2)

        n = len(items)
        for i, (name, key) in enumerate(items):
            row = f"{name:<70}{key:>5}"
            r, g, b = lerp_color("#4ea8ff", "#7f88ff", i / n if n else 0)
            print(center_line(colorize(row, r, g, b), width))
            print()

        print("\n")

        manage_inp = input("enter a letter: ").strip().lower()
        if manage_inp == "q":
            break
        run(manage_inp, width)
        time.sleep(1)


if __name__ == "__main__":
    main()