import core.todo
from core import storage


def _run(width=80):
    todo = storage.load("todo.json")
    core.todo.manage_tasks(todo, width)
    return todo


def test_add_tasks(isolated_data_dir, scripted_input):
    scripted_input(["add", "buy milk", "add", "walk", "quit"])
    todo = _run()
    assert todo == ["buy milk", "walk"]
    assert storage.load("todo.json") == todo


def test_delete_valid(isolated_data_dir, scripted_input):
    tasks = storage.load("todo.json")
    tasks.extend(["a", "b", "c"])
    storage.save("todo.json", tasks)
    scripted_input(["del 2", "quit"])
    todo = _run()
    assert todo == ["a", "c"]
    assert storage.load("todo.json") == todo


def test_delete_invalid_index(isolated_data_dir, scripted_input, capsys):
    storage.save("todo.json", ["a"])
    scripted_input(["del 99", "del 0", "quit"])
    todo = _run()
    assert todo == ["a"]
    out = capsys.readouterr().out
    assert out.count("invalid index") == 2


def test_delete_non_numeric_index(isolated_data_dir, scripted_input, capsys):
    storage.save("todo.json", ["a"])
    scripted_input(["del abc", "quit"])
    todo = _run()
    assert todo == ["a"]
    assert "please enter a valid number" in capsys.readouterr().out


def test_delete_missing_index(isolated_data_dir, scripted_input, capsys):
    scripted_input(["del", "quit"])
    todo = _run()
    assert todo == []
    assert "index not found" in capsys.readouterr().out


def test_edit_valid(isolated_data_dir, scripted_input):
    storage.save("todo.json", ["old"])
    scripted_input(["edit 1", "new task", "quit"])
    todo = _run()
    assert todo == ["new task"]
    assert storage.load("todo.json") == todo


def test_edit_out_of_range_rejected(isolated_data_dir, scripted_input, capsys):
    storage.save("todo.json", ["only"])
    scripted_input(["edit 5", "replacement", "quit"])
    todo = _run()
    assert todo == ["only"]
    assert "invalid index" in capsys.readouterr().out


def test_edit_empty_text_rejected(isolated_data_dir, scripted_input, capsys):
    storage.save("todo.json", ["keep"])
    scripted_input(["edit 1", "", "quit"])
    todo = _run()
    assert todo == ["keep"]
    assert "task cannot be empty" in capsys.readouterr().out


def test_add_empty_task_rejected(isolated_data_dir, scripted_input, capsys):
    scripted_input(["add", "", "quit"])
    todo = _run()
    assert todo == []
    assert "task cannot be empty" in capsys.readouterr().out


def test_unknown_command_reported(isolated_data_dir, scripted_input, capsys):
    scripted_input(["bogus", "quit"])
    todo = _run()
    assert todo == []
    assert "unknown command" in capsys.readouterr().out


def test_state_consistent_between_memory_and_disk(
    isolated_data_dir, scripted_input
):
    scripted_input(["add", "alpha", "add", "beta", "del 1", "quit"])
    todo = _run()
    assert todo == storage.load("todo.json")
