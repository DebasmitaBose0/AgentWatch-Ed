"""Unit tests for the CLI diagnose command logic."""

from __future__ import annotations

from agentwatch.cli.diagnose import run_diagnostics


def test_diagnostics_scan():
    report = run_diagnostics()
    assert "status" in report
    assert "packages" in report
    assert "pydantic" in report["packages"]
