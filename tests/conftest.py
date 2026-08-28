import pytest
import time

from core import plugins, storage


@pytest.fixture(autouse=True)
def isolated_data_dir(tmp_path, monkeypatch):
    """Redirect all storage writes into the test's temp directory."""
    monkeypatch.setattr(storage, "DATA_DIR", tmp_path)
    return tmp_path


@pytest.fixture(autouse=True)
def clean_registry():
    plugins.reset()
    yield
    plugins.reset()


@pytest.fixture(autouse=True)
def fast_sleep(monkeypatch):
    """Keep delayed CLI feedback from slowing the test suite down."""
    monkeypatch.setattr(time, "sleep", lambda seconds: None)


@pytest.fixture
def scripted_input(monkeypatch):
    """Feed a script of lines to ``input()`` calls."""

    def factory(script):
        lines = iter(script)

        def fake_input(prompt=""):
            return next(lines)

        monkeypatch.setattr("builtins.input", fake_input)
        return fake_input

    return factory