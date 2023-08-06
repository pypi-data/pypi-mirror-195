import cwbtasks


def test_version(capsys):
    cwbtasks.cli.version()
    output = capsys.readouterr().out.rstrip()
    assert output == f"{cwbtasks.__app_name__} v{cwbtasks.__version__}"
