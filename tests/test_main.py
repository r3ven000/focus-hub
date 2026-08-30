import cli.main


def test_main_menu_renders_and_quits_on_q(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda prompt="": "q")
    cli.main.main()
    out = capsys.readouterr().out
    assert "pomodoro timer" in out
    assert "to-do" in out
    assert "habit tracker" in out
    assert "quit" in out


def test_unknown_menu_key_does_not_crash(monkeypatch, capsys):
    keys = iter(["zz", "q"])

    def fake_input(prompt=""):
        return next(keys)

    monkeypatch.setattr("builtins.input", fake_input)
    cli.main.main()
    assert "command not found" in capsys.readouterr().out


def test_main_survives_ctrl_c_in_menu(monkeypatch, capsys):
    calls = {"n": 0}

    def fake_input(prompt=""):
        calls["n"] += 1
        if calls["n"] == 1:
            raise KeyboardInterrupt
        return "q"

    monkeypatch.setattr("builtins.input", fake_input)
    cli.main.main()
    assert calls["n"] == 2
    assert "quit" in capsys.readouterr().out


def test_main_exits_cleanly_on_eof(monkeypatch, capsys):
    def fake_input(prompt=""):
        raise EOFError

    monkeypatch.setattr("builtins.input", fake_input)
    cli.main.main()
    assert "habit tracker" in capsys.readouterr().out


def test_main_entry_point_show_cursor(monkeypatch):
    import runpy
    from pathlib import Path

    monkeypatch.setattr("builtins.input", lambda prompt="": "q")
    runpy.run_path(
        str(Path(__file__).resolve().parent.parent / "cli" / "main.py"),
        run_name="__main__",
    )
