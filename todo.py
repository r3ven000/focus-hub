print('Welcome to TO-DO lists in python!')

todo_list = [0]

def create_list(todo):
    while True:
        queston = input('create new task or exit?: ')
        if queston == 'exit':
            print(f'today to-do list made up: {todo}')
            break
        else:
            name_task = input(('name new task(or delete): '))
            if name_task == 'delete':
                deleter = int(input('which task should I delete?: '))
                todo.pop(deleter)
            else:
                todo.append(name_task)
                print(todo)

create_list(todo_list)
