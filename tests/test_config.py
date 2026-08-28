from core.config import (
    BREAK_TIME,
    GRADIENT_END,
    GRADIENT_START,
    WELCOME_ART,
    WORK_TIME,
)


def test_work_time_positive():
    assert WORK_TIME > 0


def test_break_time_positive():
    assert BREAK_TIME > 0


def test_welcome_art_not_empty():
    assert isinstance(WELCOME_ART, str)
    assert WELCOME_ART.strip()


def test_gradient_colors_are_hex():
    assert GRADIENT_START.startswith("#")
    assert GRADIENT_END.startswith("#")