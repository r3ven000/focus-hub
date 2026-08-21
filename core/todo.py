from .utils import get_terminal_width, clear_screen
from .storage import save
import time


def manage_tasks(todo, width):
    while True:
        clear_screen()
        width = get_terminal_width()
        print(
            """
    Interactive todo list manager.
    
    Commands:
    - add: Add a new task
    - del <index>: Delete task at index
    - edit <index>: Edit task at index
    - quit: Return to main menu
        """.center(width)
        )

        print("\n" + " TASKS ".center(width, "="))
        for index, task in enumerate(todo, start=1):
            task_str = f"{index}. {task}"
            print(task_str.center(width))
        if not todo:
            print("there are no tasks yet".center(width))
            print("=" * width + "\n")

        print("""

        """)

        multi_task = input("add / del / edit / quit : ".center(width)).strip()

        parts = multi_task.split()

        if not parts:
            continue
        command = parts[0].lower()

        # quit
        if command == "quit":
            break

        # del
        elif command == "del":
            if len(parts) > 1:
                try:
                    idx = int(parts[1]) - 1
                    if 0 <= idx < len(todo):
                        todo.pop(idx)
                        save("todo.json", todo)
                    else:
                        print("invalid index".center(width))
                except ValueError:
                    print("please enter a valid number".center(width))
                    time.sleep(1)
            else:
                print("index not found, try again")
                time.sleep(1)
        # edit
        elif command == "edit":
            try:
                if len(parts) > 1:
                    idx = int(parts[1]) - 1
                    new_text_task = input("enter new text task: ")
                    if new_text_task:
                        if 0 <= idx < len(todo):
                            todo[idx] = new_text_task
                            save("todo.json", todo)
                else:
                    print("invalid index".center(width))
                    time.sleep(1)
            except ValueError:
                print("please enter a valid number")
                time.sleep(1)

        # add task
        elif command == "add":
            new_task = input("enter task: ").strip()
            if new_task:
                todo.append(new_task)
                save("todo.json", todo)
            else:
                print("task cannot be empty".center(width))
                time.sleep(1)
