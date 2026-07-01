"""Unit tests for the Coverage Guard scripts."""

from __future__ import annotations

import subprocess
import sys


def test_coverage_guard_script_runs():
    res = subprocess.run([sys.executable, "scripts/verify_coverage.py"], capture_output=True, text=True)
    assert res.returncode == 0
    assert "Verifying critical module" in res.stdout
