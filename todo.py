import pyfiglet

import os
import time
welcome = pyfiglet.figlet_format('POMITRACK')

todo_list = [0]


def create_list(todo):
    while True:
        width = os.get_terminal_size().columns

        queston = input('create new task or exit?: ')
        if queston == 'exit':
            print(f'today to-do list made up: {todo}')
            print(f'today to-do list made up:')
            for index, task in enumerate(todo):
                if task != 0:
                    print(f'{index}. {task}'.center(width))
            break
        else:
            name_task = input('task / del / edit / exit ').strip()
            if name_task == 'delete':
                deleter = int(input('which task should I delete?: '))
                todo.pop(deleter)
            else:
                todo.append(name_task)
                print(todo)
                print("\n" + " TASKS ".center(width, "="))
                has_tasks = False
                for index, task in enumerate(todo):
                    if task != 0:
                        task_str = f'{index}. {task}'
                        print(task_str.center(width))
                        has_tasks = True
                if not has_tasks:
                    print('there are no tasks yet'.center(width))
                print('=' * width + '\n')


def timer(minutes):
    seconds = minutes * 60
    while seconds > 0:
        mins, secs = divmod(seconds, 60)
        timer_str = f"Remaining: {mins:02d}:{secs:02d}"
        print(timer_str.center(width), end='\r')
        time.sleep(1)
        seconds -= 1
    print("Time's up".center(width))

manager = {
    't': create_list,
    'p': lambda todo: timer(25)
}
width = os.get_terminal_size().columns

for line in welcome.split('\n'):
    if line.strip():
        print(line.center(width))
while True:
    width = os.get_terminal_size().columns
    print(""" 
   pomidoro timer                                        p
   to-do                                                 t
""".center(width))

    manage_inp = input('enter your task: ').strip()
    if manage_inp == 'exit':
        break
    action = manager.get(manage_inp)
    if action:
        action(todo_list)
    else:
        print('command not found!'.center(width))
print(welcome)
