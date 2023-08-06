from typer.testing import CliRunner

from .__main__ import app

runner = CliRunner()


def test_app_show_all():
    result = runner.invoke(app, ["--show", "all", "Pinguin"])
    assert "Scratch" in result.stdout


def test_app_check_only():
    result = runner.invoke(app, ["--show", "all", "--check-only", "Scratch", "Pinguin"])
    assert "Scratch" in result.stdout
