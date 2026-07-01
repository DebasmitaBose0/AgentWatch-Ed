"""Integration tests for SemanticCache integration with watch()."""

from __future__ import annotations

import pytest
from agentwatch import watch
from agentwatch.core.watcher import GenericAdapter


class DummyAgent:
    def __init__(self):
        self.calls = 0

    def run(self, prompt: str) -> str:
        self.calls += 1
        return f"Response to {prompt}"


def test_watcher_semantic_cache_integration():
    agent = DummyAgent()
    watched = watch(agent)

    # First run (cache miss, executes original method)
    res1 = watched.run("Check compliance residency records.")
    assert res1 == "Response to Check compliance residency records."
    assert agent.calls == 1

    # Second run (exact match - cache hit, should NOT call original method)
    res2 = watched.run("Check compliance residency records.")
    assert res2 == "Response to Check compliance residency records."
    assert agent.calls == 1

    # Third run (semantic match - cache hit, should NOT call original method)
    res3 = watched.run("Check compliance residency records detail.")
    assert res3 == "Response to Check compliance residency records."
    assert agent.calls == 1
