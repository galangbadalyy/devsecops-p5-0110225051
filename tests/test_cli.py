from taskmanager.cli import run


def test_cli_add_list_stats(tmp_path, capsys):
    f = str(tmp_path / "t.json")
    assert run(["--file", f, "add", "Coba CLI", "--priority", "high"]) == 0
    assert run(["--file", f, "list"]) == 0
    out = capsys.readouterr().out
    assert "Coba CLI" in out


def test_cli_error(tmp_path, capsys):
    f = str(tmp_path / "t.json")
    assert run(["--file", f, "done", "99"]) == 1
