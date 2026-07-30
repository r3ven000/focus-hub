
#imports
import pyfiglet
import os
import time
welcome = pyfiglet.figlet_format('POMITRACK')

todo_list = [0]


#todo function
def create_list(todo):
    while True:
        width = os.get_terminal_size().columns #setting

        multi_task = input('task / del / edit / exit : '.center(width)).strip()
        
        parts = multi_task.split()
        if not parts:
            continue
        command = parts[0].lower()

        if command == 'exit':
            elif command == 'del':

            if len(parts) > 1:

                idx = int(parts[1])
                todo.pop(idx)

        elif command == 'edit':
            if len(parts) > 1:
                idx = int(parts[1])
                new_text_task = input('enter new text task: ')
                todo[idx] = new_text_task
            else:
                todo.append(name_task)
                print("\n" + " TASKS ".center(width, "="))
@@ -45,10 +56,12 @@ def timer(minutes):
        time.sleep(1)
        seconds -= 1
    print("Time's up".center(width))

def pomidoro(todo):
    timer(25)
    timer(5)
manager = {
    't': create_list,
    'p': lambda todo: timer(25)
    'p': pomidoro
}
width = os.get_terminal_size().columns

@@ -73,3 +86,5 @@ def timer(minutes):
print(welcome)



