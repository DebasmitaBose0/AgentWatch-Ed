"""Integration tests for the CLI diagnose command."""

from __future__ import annotations

from typer.testing import CliRunner
from agentwatch.cli.main import app

runner = CliRunner()


def test_cli_diagnose_command():
    result = runner.invoke(app, ["diagnose"])
    assert result.exit_code == 0
    assert "Running AgentWatch Diagnostics" in result.stdout
    assert "Installed Packages" in result.stdout
