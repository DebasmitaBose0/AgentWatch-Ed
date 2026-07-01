"""Integration tests for Client-Side Rate Limiting inside watch()."""

from __future__ import annotations

import time
import pytest
from unittest.mock import MagicMock
from agentwatch import watch
from agentwatch.core.watcher import GenericAdapter


class DummyAgent:
    def __init__(self):
        self.calls = 0

    def run(self) -> str:
        self.calls += 1
        return "success"


def test_watcher_rate_limiter_integration(monkeypatch):
    # Mock event bus publishing to avoid slow HTTP/Redis calls in tests
    monkeypatch.setattr("agentwatch.core.watcher.get_event_bus", lambda: MagicMock())

    agent = DummyAgent()
    watched = watch(agent)
    
    # Mock _emit_safely and _async_emit to avoid any real network logs
    watched._agentwatch_adapter._emit_safely = MagicMock()
    watched._agentwatch_adapter._async_emit = MagicMock()

    # Force low capacity rate limiter for testing
    from agentwatch.core.rate_limiter import ClientRateLimiter
    watched._agentwatch_adapter._rate_limiter = ClientRateLimiter(requests_per_minute=2)

    # First two calls should succeed immediately
    t0 = time.monotonic()
    assert watched.run() == "success"
    assert watched.run() == "success"
    dur = time.monotonic() - t0
    assert dur < 0.1

    # Third call should hit rate limit and trigger sleep/delay
    t1 = time.monotonic()
    assert watched.run() == "success"
    dur2 = time.monotonic() - t1
    assert dur2 >= 0.04
