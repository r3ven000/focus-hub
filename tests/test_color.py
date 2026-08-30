from core.color import center_line, colorize, lerp_color, tint, tint_center
from core.config import GRADIENT_END, GRADIENT_START


def test_center_line_strips_ansi_when_padding():
    colored = colorize("hi", 1, 2, 3)
    line = center_line(colored, 10)
    assert line.startswith("    ")
    assert line.endswith("hi\x1b[0m")


def test_center_line_with_plain_text():
    assert center_line("abcd", 10) == "   abcd"


def test_lerp_color_endpoints():
    assert lerp_color("#000000", "#ffffff", 0.0) == (0, 0, 0)
    assert lerp_color("#000000", "#ffffff", 1.0) == (255, 255, 255)


def test_lerp_color_midpoint():
    assert lerp_color("#ff0000", "#0000ff", 0.5) == (128, 0, 128)


def test_tint_wraps_text_with_truecolor():
    out = tint("hello", 0.5)
    assert out.startswith("\x1b[38;2;")
    assert out.endswith("hello\x1b[0m")


def test_tint_midpoint_blends_gradient():
    r, g, b = lerp_color(GRADIENT_START, GRADIENT_END, 0.5)
    assert tint("x", 0.5) == colorize("x", r, g, b)


def test_tint_center_pads_visible_text():
    line = tint_center("ab", 10)
    assert line.startswith("    \x1b[38;2;")
    assert line.endswith("ab\x1b[0m")
