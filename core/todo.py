from .list_manager import GenericListManager

_TODO_MANAGER: GenericListManager = GenericListManager(
    filename="todo.json",
    label="task",
    heading="Interactive todo list manager.",
)


def manage_tasks(todo: list[str], width: int) -> None:
    """Run the interactive task editor, mutating ``todo`` and saving to disk."""
    _TODO_MANAGER.run_list(todo, width)