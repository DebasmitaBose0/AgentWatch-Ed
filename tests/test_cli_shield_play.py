"""Unit tests for the CLI safety play command logic."""

from __future__ import annotations

from unittest.mock import patch, MagicMock
from agentwatch.cli.shield_play import start_safety_playground


@patch("agentwatch.cli.shield_play.input", create=True)
def test_safety_playground_exit(mock_input):
    mock_input.side_effect = ["exit"]
    # Should terminate immediately
    start_safety_playground()
