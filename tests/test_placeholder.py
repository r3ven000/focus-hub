from core.placeholder import in_dev


def test_in_dev_prints_notice(capsys):
    in_dev(80)
    assert "function in dev!" in capsys.readouterr().out