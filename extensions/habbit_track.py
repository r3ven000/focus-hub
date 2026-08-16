from core.utils import get_terminal_width, clear_screen


def habbits_manage(habbit):
    pass


def habbit_tracker(habbit, width):
    while True:
        width = get_terminal_width()
        clear_screen()

        print(
            """
    Interactive habbit track manager.
    
    Commands:
    - add: Add a new habbit
    - next: 
    - del <index>: Delete habbit at index
    - edit <index>: Edit habbit at index
    - quit: Return to main menu
        """.center(width)
        )
        print("\n" + " habbits list ".center(width, "="))
        for index, habit in enumerate(habbit, start=1):
            habbit_str = f"{index}. {habit}"
            print(habbit_str.center(width))
        if not habbit:
            print("there are no habbits yet".center(width))
            print("=" * width + "\n")

        print("""


        """)
        multi_habbit = input("add / next / del / edit / quit : ".center(width)).strip()

        parts = multi_habbit.split()
        # parts-[habbit, number]

        if not parts:
            continue
        command = parts[0].lower()
        # command-[habbit(add, next, del, edit, quit)]

        # quit
        if command == "quit":
            break

        # del
        elif command == "del":
            if len(parts) > 1:  # [habbit(1-st) , number(2-nd)]
                try:
                    idx = int(parts[1]) - 1  # index habbit in habbits_list
                    if 0 <= idx < len(habbit):
                        habbit.pop(idx)
                    else:
                        print("invalid index".center(width))
                except ValueError:
                    print("please enter a valid number".center(width))
        # edit
        elif command == "edit":
            try:
                if len(parts) > 1:
                    idx = int(parts[1]) - 1  # index '2' in 2 (int)
                    new_text_habbit = input("enter new text habbit: ")
                    if new_text_habbit:
                        habbit[idx] = new_text_habbit
                else:
                    print("invalid index".center(width))
            except IndexError:
                print("please enter a valid number")

        # add habbit
        elif command == "add":
            new_habbit = input("enter habbit: ").strip()
            if new_habbit:
                habbit.append(new_habbit)
            else:
                print("habbit cannot be empty".center(width))
