"""Integration tests for the CLI safety play command."""

from __future__ import annotations

from typer.testing import CliRunner
from agentwatch.cli.main import app

runner = CliRunner()


def test_cli_safety_play_command():
    result = runner.invoke(app, ["safety", "play"], input="rm -rf /\nexit\n")
    assert result.exit_code == 0
    assert "🛡️ AGENTWATCH SHIELD PLAYGROUND 🛡️" in result.stdout
    assert "BLOCKED" in result.stdout
