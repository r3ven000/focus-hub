import pyfiglet
import os
import time
welcome = pyfiglet.figlet_format('POMITRACK')
welcome = pyfiglet.figlet_format('POMOTRACK')

todo_list = [0]
todo_list = []

#todo function
def create_list(todo):
def manage_tasks(todo):
    while True:
        width = os.get_terminal_size().columns #setting
        def get_terminal_width():
            return os.get_terminal_size().columns
        width = get_terminal_width()
        print("""
    Interactive todo list manager.
    
    Commands:
    - task: Add a new task
    - del <index>: Delete task at index
    - edit <index>: Edit task at index
    - exit: Return to main menu
        """.center(width))

        multi_task = input('task / del / edit / exit : '.center(width)).strip()

@@ -44,8 +55,12 @@ def create_list(todo):
            except IndexError:
                print('please enter a valid number')

        else:
            todo.append(multi_task)
        elif command == 'add':
            new_task = input('enter task: ').strip()
            if new_task:
                todo.append(new_task)
            else:
                print('task cannot be empty'.center(width))  
            print("\n" + " TASKS ".center(width, "="))
            has_tasks = False
            for index, task in enumerate(todo):
@@ -59,20 +74,25 @@ def create_list(todo):


def timer(minutes):
    seconds = minutes * 60
    while seconds > 0:
        mins, secs = divmod(seconds, 60)
        timer_str = f"Remaining: {mins:02d}:{secs:02d}"
    end_time = time.time() + (minutes * 60)
    while time.time() < end_time:
        remaining = end_time - time.time()
        mins, secs = divmod(int(remaining), 60)
        timer_str = f'remaining: {mins:02d}:{secs:02d}'
        print(timer_str.center(width), end='\r')
        time.sleep(1)
        seconds -= 1
    print("Time's up".center(width))
def pomidoro(todo):
    timer(25)
    timer(5)
        time.sleep(0.1)
    print("time's up".center(width))

work_time = 25
break_time = 5
def pomodoro(todo, width):
    print('starting work session...'.center(width))
    timer(work_time, width)
    print('starting break...'.center(get_terminal_width))
    timer(break_time, width)
manager = {
    't': create_list,
    'p': pomidoro
    't': manage_tasks,
    'p': pomodoro
}
width = os.get_terminal_size().columns

@@ -82,18 +102,20 @@ def pomidoro(todo):
while True:
    width = os.get_terminal_size().columns
    print(""" 
   pomidoro timer                                        p
   pomodoro timer                                        p
   to-do                                                 t
   quit                                                  q
""".center(width))

    manage_inp = input('enter your task: ').strip()
    if manage_inp == 'exit':
    manage_inp = input('enter a letter: ').strip()
    if manage_inp == 'q':
        break
    action = manager.get(manage_inp)
    if action:
        action(todo_list)
        action(manage_tasks)
    else:
        print('command not found!'.center(width))
print(welcome)
