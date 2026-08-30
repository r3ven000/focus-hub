import pytest

import core.settings as settings_module
from core import config, plugins, storage
from core.settings import (
    DEFAULT_SETTINGS,
    SettingsManager,
    apply_settings,
    enabled_extensions,
    is_valid_hex,
    load_settings,
    preview_gradient,
    save_settings,
    settings_menu,
)


@pytest.fixture(autouse=True)
def restore_gradient():
    """Keep the global config palette intact between tests."""
    start = config.GRADIENT_START
    end = config.GRADIENT_END
    yield
    config.GRADIENT_START = start
    config.GRADIENT_END = end


def test_is_valid_hex():
    assert is_valid_hex("#4ea8ff")
    assert is_valid_hex("#FFFFFF")
    assert not is_valid_hex("#fff")  # too short
    assert not is_valid_hex("4ea8ff")  # missing #
    assert not is_valid_hex("#12345g")  # non-hex digit


def test_load_settings_returns_defaults_when_no_file():
    settings = load_settings()
    assert settings["gradient_start"] == DEFAULT_SETTINGS["gradient_start"]
    assert settings["gradient_end"] == DEFAULT_SETTINGS["gradient_end"]


def test_load_settings_merges_saved_values():
    save_settings(
        {"gradient_start": "#ff0000", "gradient_end": "#00ff00", "extra": 1}
    )
    settings = load_settings()
    assert settings["gradient_start"] == "#ff0000"
    assert settings["gradient_end"] == "#00ff00"
    assert settings["extra"] == 1


def test_corrupt_settings_file_falls_back_to_defaults(capsys):
    storage.save("settings.json", "not a dict at all")
    settings = load_settings()
    assert settings["gradient_start"] == DEFAULT_SETTINGS["gradient_start"]
    assert "settings.json is corrupt" in capsys.readouterr().out


def test_apply_settings_updates_config():
    apply_settings({"gradient_start": "#ff0000", "gradient_end": "#00ff00"})
    assert config.GRADIENT_START == "#ff0000"
    assert config.GRADIENT_END == "#00ff00"


def test_apply_settings_ignores_invalid_values():
    apply_settings({"gradient_start": "nope", "gradient_end": ""})
    assert config.GRADIENT_START == DEFAULT_SETTINGS["gradient_start"]
    assert config.GRADIENT_END == DEFAULT_SETTINGS["gradient_end"]


def test_apply_settings_reaches_tint():
    from core.color import tint

    apply_settings({"gradient_start": "#000000", "gradient_end": "#ffffff"})
    assert tint("x", 1.0).startswith("\x1b[38;2;255;255;255m")


def test_enabled_extensions_none_by_default():
    assert enabled_extensions() is None


def test_enabled_extensions_returns_stored_list():
    save_settings({"enabled_extensions": ["habit_track", "other"]})
    assert enabled_extensions() == ["habit_track", "other"]


def test_preview_gradient_is_colored_line():
    line = preview_gradient(config.GRADIENT_START, config.GRADIENT_END, 10)
    assert line.startswith("\x1b[38;2;")
    assert len(line) > 10


def test_settings_menu_renders_and_quits(capsys, scripted_input):
    scripted_input(["3"])
    settings_menu(80)
    out = capsys.readouterr().out
    assert "colors" in out
    assert "extensions" in out
    assert "quit" in out


def test_colors_menu_sets_and_saves(capsys, scripted_input):
    scripted_input(["1", "1 #ff0000", "3", "3"])
    settings_menu(80)
    assert storage.load("settings.json", default={})["gradient_start"] == "#ff0000"
    assert config.GRADIENT_START == "#ff0000"
    assert "top color set to #ff0000" in capsys.readouterr().out


def test_colors_menu_rejects_invalid(capsys, scripted_input):
    scripted_input(["1", "top nope", "3", "3"])
    settings_menu(80)
    assert "invalid color, use #RRGGBB" in capsys.readouterr().out
    assert config.GRADIENT_START == DEFAULT_SETTINGS["gradient_start"]


def test_extensions_toggle_off(capsys, scripted_input):
    scripted_input(["2", "1", "q", "3"])
    settings_menu(80)
    assert storage.load("settings.json", default={})["enabled_extensions"] == []
    assert "habit_track is now disabled" in capsys.readouterr().out
    assert enabled_extensions() == []


def test_extensions_toggle_back_to_all(capsys, scripted_input):
    save_settings({"enabled_extensions": []})
    scripted_input(["2", "1", "q", "3"])
    settings_menu(80)
    assert "habit_track is now enabled" in capsys.readouterr().out
    assert enabled_extensions() is None


def test_plugins_available_extensions(tmp_path):
    (tmp_path / "hello.py").write_text("", encoding="utf-8")
    (tmp_path / "__init__.py").write_text("", encoding="utf-8")
    assert plugins.available_extensions(tmp_path) == ["hello"]


def test_load_plugins_respects_enabled_filter(tmp_path):
    hello = tmp_path / "hello.py"
    hello.write_text(
        "from core.plugins import register\n"
        "@register(name='hello', key='z', description='x')\n"
        "def run(width):\n    pass\n",
        encoding="utf-8",
    )
    world = tmp_path / "world.py"
    world.write_text(
        "from core.plugins import register\n"
        "@register(name='world', key='w', description='x')\n"
        "def run(width):\n    pass\n",
        encoding="utf-8",
    )
    plugins.load_plugins(tmp_path, enabled=["hello"])
    assert plugins.get_plugin("z") is not None
    assert plugins.get_plugin("w") is None


def test_settings_menu_reached_through_plugin_key(scripted_input):
    plugins.load_builtins()
    scripted_input(["3"])
    assert plugins.run("s", 80) is True


def test_settings_manager_constructs_with_defaults():
    mgr = SettingsManager()
    assert mgr.filename == "settings.json"
    assert mgr.title == "settings"


def test_settings_menu_ignores_empty_input(capsys, scripted_input):
    scripted_input(["", "3"])
    settings_menu(80)
    out = capsys.readouterr().out
    assert "colors" in out


def test_settings_menu_unknown_command(capsys, scripted_input):
    scripted_input(["xyz", "3"])
    settings_menu(80)
    assert "unknown command" in capsys.readouterr().out


def test_colors_menu_ignores_empty_input(capsys, scripted_input):
    scripted_input(["1", "", "3", "3"])
    settings_menu(80)
    assert "unknown command" not in capsys.readouterr().out


def test_colors_menu_unknown_command(capsys, scripted_input):
    scripted_input(["1", "xyz", "3", "3"])
    settings_menu(80)
    assert "unknown command" in capsys.readouterr().out


def test_colors_menu_prompts_for_color(capsys, scripted_input):
    scripted_input(["1", "1", "#00ff00", "3", "3"])
    settings_menu(80)
    assert storage.load("settings.json", default={})["gradient_start"] == "#00ff00"
    assert "top color set to #00ff00" in capsys.readouterr().out


def test_extensions_menu_handles_non_numeric_toggle(capsys, scripted_input):
    scripted_input(["2", "abc", "q", "3"])
    settings_menu(80)
    assert "unknown command" in capsys.readouterr().out


def test_extensions_menu_rejects_out_of_range(capsys, scripted_input):
    scripted_input(["2", "99", "q", "3"])
    settings_menu(80)
    assert "invalid index" in capsys.readouterr().out


def test_extensions_menu_no_extensions(capsys, scripted_input, monkeypatch):
    monkeypatch.setattr(settings_module, "_available_extensions", lambda: [])
    scripted_input(["2", "q", "3"])
    settings_menu(80)
    assert "no extensions found" in capsys.readouterr().out
