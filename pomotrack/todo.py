from utils import get_terminal_width, clear_screen

def manage_tasks(todo, width):
    while True:
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



