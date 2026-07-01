"""Unit tests for the Bandit Security Audit runner script."""

from __future__ import annotations

import subprocess
import sys


def test_bandit_audit_script_execution():
    result = subprocess.run(
        [sys.executable, "scripts/run_bandit_audit.py"],
        capture_output=True,
        text=True
    )
    # Output should print the scanner starting log
    assert "Executing security check scan" in result.stdout
    assert result.returncode == 0
