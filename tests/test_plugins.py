import textwrap

from core import plugins, storage


def _make_extension(tmp_path, filename, body):
    path = tmp_path / filename
    path.write_text(textwrap.dedent(body), encoding="utf-8")
    return path


def test_register_decorator_registers_plugin():
    @plugins.register("demo", "d", "A demo plugin")
    def run(width):
        return 42

    plugin = plugins.get_plugin("d")
    assert plugin is not None
    assert plugin.name == "demo"
    assert plugin.description == "A demo plugin"
    assert plugin.handler(80) == 42


def test_register_uses_function_doc_as_description():
    @plugins.register("demo", "e")
    def run(width):
        """docstring description"""
        pass

    assert plugins.get_plugin("e").description == "docstring description"


def test_duplicate_key_is_skipped(capsys):
    @plugins.register("first", "x", "first")
    def one(width):
        pass

    @plugins.register("second", "x", "second")
    def two(width):
        pass

    assert plugins.get_plugin("x").name == "first"
    assert "already taken" in capsys.readouterr().out


def test_load_plugins_from_directory(tmp_path):
    _make_extension(
        tmp_path,
        "hello.py",
        """
        from core.plugins import register

        @register(name="hello world", key="z", description="Greets the user")
        def run(width):
            pass
        """,
    )
    plugins.load_plugins(tmp_path)
    plugin = plugins.get_plugin("z")
    assert plugin is not None
    assert plugin.name == "hello world"
    assert plugin.key == "z"


def test_load_plugins_ignores_init(tmp_path):
    (tmp_path / "__init__.py").write_text(
        textwrap.dedent(
            """
            from core.plugins import register

            @register(name="init plugin", key="i", description="should not load")
            def run(width):
                pass
            """
        ),
        encoding="utf-8",
    )
    plugins.load_plugins(tmp_path)
    assert plugins.get_plugin("i") is None


def test_broken_plugin_is_reported_and_skipped(tmp_path, capsys):
    _make_extension(tmp_path, "broken.py", "raise RuntimeError('boom')\n")
    plugins.load_plugins(tmp_path)
    assert "failed to load broken.py" in capsys.readouterr().out


def test_run_dispatches_handler():
    captured = {}

    @plugins.register("cap", "c", "captures width")
    def run(width):
        captured["width"] = width

    assert plugins.run("c", 44) is True
    assert captured == {"width": 44}


def test_run_unknown_command_returns_false(capsys):
    assert plugins.run("nope", 80) is False
    assert "command not found" in capsys.readouterr().out


def test_run_handler_exception_is_caught(capsys):
    @plugins.register("boom", "b", "always raises")
    def run(width):
        raise ValueError("kaboom")

    assert plugins.run("b", 80) is False
    assert "[boom] error: kaboom" in capsys.readouterr().out


def test_menu_items_preserve_order():
    @plugins.register("first", "a", "first")
    def first(width):
        pass

    @plugins.register("second", "b", "second")
    def second(width):
        pass

    assert plugins.menu_items() == [("first", "a"), ("second", "b")]


def test_load_builtins_registers_core_commands():
    plugins.load_builtins()
    keys = {key for _, key in plugins.menu_items()}
    assert {"p", "t", "j", "o", "s"} <= keys


def test_load_builtins_is_idempotent():
    plugins.load_builtins()
    plugins.load_builtins()
    assert len(plugins.menu_items()) == 5


def test_real_extension_discovered_from_repo():
    plugins.load_plugins()
    plugin = plugins.get_plugin("h")
    assert plugin is not None
    assert plugin.name == " habit tracker"


def test_builtin_todo_handler_persists(isolated_data_dir, scripted_input):
    plugins.load_builtins()
    scripted_input(["add", "buy milk", "quit"])
    assert plugins.run("t", 80) is True
    assert storage.load("todo.json") == ["buy milk"]


def test_import_extension_skips_non_python_file(tmp_path):
    path = tmp_path / "notes.txt"
    path.write_text("print('hi')\n", encoding="utf-8")
    plugins._import_extension(path)
    assert plugins.menu_items() == []


def test_available_extensions_missing_dir_returns_empty(tmp_path):
    assert plugins.available_extensions(tmp_path / "nope") == []


def test_load_plugins_missing_dir_is_noop(tmp_path):
    plugins.load_plugins(tmp_path / "nope")
    assert plugins.menu_items() == []
