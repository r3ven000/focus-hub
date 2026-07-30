from utils import clear_screen, get_terminal_width, in_dev
from todo import manage_tasks
from pomodoro import pomodoro
from habbit_track import habbits_manage, habbit_tracker
from config import WELCOME_ART, ITEMS_MENU
import os
import time

todo_list = []
habbit_list = []

manager = {
    't': manage_tasks,
    'p': pomodoro,
    'h': habbit_tracker,
    'd': in_dev,
    'j': in_dev,
    'o': in_dev,
    's': in_dev
}

def main():
    while True:
        clear_screen()
        width = get_terminal_width()
        height = os.get_terminal_size().lines
        content_height = 5 + (len(ITEMS_MENU) * 2)
        top_padding = max(1, ((height - content_height) // 2) - 5)
        print('\n' * top_padding)
        for line in WELCOME_ART.split('\n'):
            if line.strip():
                print(line.center(width))

        print('\n' * 2)

        for name, key in ITEMS_MENU:
            row = f'{name:<65}{key:>5}'
            print(row.center(width))
            print()

        print('\n')

        manage_inp = input('enter a letter: ').strip()
        if manage_inp == 'q':
            break
        action = manager.get(manage_inp) #func in manager
        if action:
            action(todo_list, width)
            if action == in_dev:
                time.sleep(2)
        else:
            print('command not found!'.center(width))
            time.sleep(2)
    print(WELCOME_ART)

    



if __name__ == "__main__":
    main()
