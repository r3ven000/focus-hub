#Early versions of the project can be found in my repository learn python / practice / function def /06_todo.py
#imports
import pyfiglet
from pyfiglet import Figlet, FigletFont
import os
import time

welcome = r"""
██████╗  ██████╗ ███╗   ███╗ ██████╗ ████████╗██████╗  █████╗  ██████╗██╗  ██╗
██╔══██╗██╔═══██╗████╗ ████║██╔═══██╗╚══██╔══╝██╔══██╗██╔══██╗██╔════╝██║ ██╔╝
██████╔╝██║   ██║██╔████╔██║██║   ██║   ██║   ██████╔╝███████║██║     █████╔╝ 
██╔═══╝ ██║   ██║██║╚██╔╝██║██║   ██║   ██║   ██╔══██╗██╔══██║██║     ██╔═██╗ 
██║     ╚██████╔╝██║ ╚═╝ ██║╚██████╔╝   ██║   ██║  ██║██║  ██║╚██████╗██║  ██╗
╚═╝      ╚═════╝ ╚═╝     ╚═╝ ╚═════╝    ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝
                                                                              
"""
#welcome = figlet_object.renderText('POMOTRACK')

todo_list = []

#in dev function
def in_dev(*args, **kwargs):
    width = os.get_terminal_size().columns
    print('function in dev!'.center(width))
    

#todo function
def manage_tasks(todo, width):
    while True:
        def get_terminal_width():
            return os.get_terminal_size().columns
        width = get_terminal_width()
        print("""
    Interactive todo list manager.
    
    Commands:
    - add: Add a new task
    - del <index>: Delete task at index
    - edit <index>: Edit task at index
    - quit: Return to main menu
        """.center(width))

        multi_task = input('add / del / edit / quit : '.center(width)).strip()
        
        parts = multi_task.split()
        #parts-[task, number]
        
        if not parts:
            continue
        command = parts[0].lower()
        #command-[task(add, del, edit, quit)]

        #quit
        if command == 'quit':
            break

        #del
        elif command == 'del':

            if len(parts) > 1: #[task(1-st) , number(2-nd)]
                try:
                    idx = int(parts[1]) #index task in todo_list
                    if 0 <= idx < len(todo):
                        todo.pop(idx)
                    else:
                        print('invalid index'.center(width))
                except ValueError:
                    print('please enter a valid number'.center(width))
        #edit
        elif command == 'edit':
            try:
                if len(parts) > 1:
                    idx = int(parts[1]) #index '2' in 2 (int)
                    new_text_task = input('enter new text task: ')
                    todo[idx] = new_text_task
                else:
                    print('invalid index'.center(width))
            except IndexError:
                print('please enter a valid number')
        
        #add task
        elif command == 'add':
            new_task = input('enter task: ').strip()
            if new_task:
                todo.append(new_task)
            else:
                print('task cannot be empty'.center(width))  
        print("\n" + " TASKS ".center(width, "="))
        has_tasks = False
        for index, task in enumerate(todo):
            if task != 0:
                task_str = f'{index}. {task}'
                print(task_str.center(width))
                has_tasks = True

            #not tasks
            if not has_tasks:
                print('there are no tasks yet'.center(width))
                print('=' * width + '\n')


def timer(minutes, width):
    end_time = time.time() + (minutes * 60)
    while time.time() < end_time:
        remaining = end_time - time.time()
        mins, secs = divmod(int(remaining), 60)
        timer_str = f'remaining: {mins:02d}:{secs:02d}'
        
        os.system('cls' if os.name == 'nt' else 'clear')
        width = os.get_terminal_size().columns
        print('\n' * 3)
        print(timer_str.center(width))
        time.sleep(0.5)
    print("time's up".center(width))

work_time = 25
break_time = 5
def pomodoro(todo, width):
    print('starting work session...'.center(width))
    timer(work_time, width)
    print('starting break...'.center(get_terminal_size().columns))
    timer(break_time, width)
manager = {
    't': manage_tasks,
    'p': pomodoro,
    'h': in_dev,
    'd': in_dev,
    'j': in_dev,
    'o': in_dev,
    's': in_dev

}
width = os.get_terminal_size().columns

while True:
    os.system('cls' if os.name == 'nt' else 'clear')
    width = os.get_terminal_size().columns
    height = os.get_terminal_size().lines
    menu_items = [ 
    ('pomodoro timer', 'p'),
    ('to-do', 't'),
    ('habbit-tracker', 'h'),
    ('diary', 'd'),
    ('import-data-to-.json', 'j'),
    ('import-data-to-Obsidian', 'o'),
    ('settings', 's'),
    ('quit', 'q')
]
    content_height = 5 + (len(menu_items) * 2)
    top_padding = max(1, ((height - content_height) // 2) - 5)
    print('\n' * top_padding)
    for line in welcome.split('\n'):
        if line.strip():
            print(line.center(width))

    print('\n' * 2)
    for name, key in menu_items:
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
print(welcome)
