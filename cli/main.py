from core.banner import render_menu
from core.color import tint, tint_center
from core.plugins import load_builtins, load_plugins, menu_items, run
from core.config import WELCOME_ART
from core.settings import apply_settings, load_settings
from core.terminal import (
    clear_screen,
    get_terminal_width,
    get_terminal_height,
    show_cursor,
)
import time


def main() -> None:
    # Pull the saved gradient palette into core.config first, so every screen
    # (menu, timers, managers) opens with the user's colors already applied.
    apply_settings(load_settings())
    load_builtins()
    load_plugins()
    while True:
        try:
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
                print(tint_center(line, width, t))

            print("\n" * 2)

            for row in render_menu(items, width):
                print(row)
                print()

            print("\n")

            manage_inp = input(tint("enter a letter: ")).strip().lower()
            if manage_inp == "q":
                break
            run(manage_inp, width)
            time.sleep(1)
        # Ctrl+C anywhere during the loop (menu input, timers, managers)
        # just redraws the menu instead of crashing the app.
        except KeyboardInterrupt:
            continue


if __name__ == "__main__":
    try:
        main()
    finally:
        show_cursor()