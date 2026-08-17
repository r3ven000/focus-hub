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
        # parts-[habit, number]

        if not parts:
            continue
        command = parts[0].lower()
        # command-[habit(add, next, del, edit, quit)]

        # quit
        if command == "quit":
            break

        # del
        elif command == "del":
            if len(parts) > 1:  # [habit(1-st) , number(2-nd)]
                try:
                    idx = int(parts[1]) - 1  # index habit in habits_list
                    if 0 <= idx < len(habit):
                        habit.pop(idx)
                        save("habits.json", habit)
                    else:
                        print("invalid index".center(width))
                except ValueError:
                    print("please enter a valid number".center(width))
        # edit
        elif command == "edit":
            try:
                if len(parts) > 1:
                    idx = int(parts[1]) - 1  # index '2' in 2 (int)
                    new_text_habit = input("enter new text habit: ")
                    if new_text_habit:
                        habit[idx] = new_text_habit
                        save("habits.json", habit)
                else:
                    print("invalid index".center(width))
            except IndexError:
                print("please enter a valid number")

        # add habit
        elif command == "add":
            new_habit = input("enter habit: ").strip()
            if new_habit:
                habit.append(new_habit)
                save("habits.json", habit)
            else:
                print("habit cannot be empty".center(width))
