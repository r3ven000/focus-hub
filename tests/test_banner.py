from core.banner import banner, print_banner, render_menu


def test_banner_defaults_to_terminal_width():
    lines = banner("test")
    assert lines
    assert all("\x1b[38;2;" in line for line in lines)


def test_render_menu_defaults_to_terminal_width():
    rows = render_menu([("add", "1"), ("quit", "4")])
    assert len(rows) == 2
    assert all(row.startswith(" ") for row in rows)


def test_print_banner_prints_gradient_lines(capsys):
    print_banner("hi")
    out = capsys.readouterr().out
    assert "\x1b[38;2;" in out