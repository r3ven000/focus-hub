from core.utils import get_terminal_width, clear_screen
from core.storage import save


def habits_manage(habit):
    pass


def habit_tracker(habit, width):
    while True:
        width = get_terminal_width()
        clear_screen()

        print(
            """
    Interactive habit track manager.
    
    Commands:
    - add: Add a new habit
    - next: 
    - del <index>: Delete habit at index
    - edit <index>: Edit habit at index
    - quit: Return to main menu
        """.center(width)
        )
        print("\n" + " habits list ".center(width, "="))
        for index, item in enumerate(habit, start=1):
            habit_str = f"{index}. {item}"
            print(habit_str.center(width))
        if not habit:
            print("there are no habits yet".center(width))
            print("=" * width + "\n")

        print("""


        """)
        multi_habit = input("add / next / del / edit / quit : ".center(width)).strip()

        parts = multi_habit.split()

        if not parts:
            continue
        command = parts[0].lower()

        # quit
        if command == "quit":
            break

        # del
        elif command == "del":
            if len(parts) <= 1:
                print("index not found, try again".center(width))
                continue
            try:
                idx = int(parts[1]) - 1
            except ValueError:
                print("please enter a valid number".center(width))
                continue
            if not 0 <= idx < len(habit):
                print("invalid index".center(width))
                continue
            habit.pop(idx)
            save("habits.json", habit)
        # edit
        elif command == "edit":
            if len(parts) <= 1:
                print("index not found, try again".center(width))
                continue
            try:
                idx = int(parts[1]) - 1
            except ValueError:
                print("please enter a valid number".center(width))
                continue
            if not 0 <= idx < len(habit):
                print("invalid index".center(width))
                continue
            new_text_habit = input("enter new text habit: ").strip()
            if not new_text_habit:
                print("habit cannot be empty".center(width))
                continue
            habit[idx] = new_text_habit
            save("habits.json", habit)

        # add habit
        elif command == "add":
            new_habit = input("enter habit: ").strip()
            if new_habit:
                habit.append(new_habit)
                save("habits.json", habit)
            else:
                print("habit cannot be empty".center(width))

        else:
            print("unknown command".center(width))
