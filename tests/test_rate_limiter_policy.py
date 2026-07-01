"""Unit tests for ClientRateLimiter and backoff algorithms."""

from __future__ import annotations

import time
import pytest
from agentwatch.core.rate_limiter import ClientRateLimiter, get_adaptive_backoff


def test_rate_limiter_acquires_tokens():
    limiter = ClientRateLimiter(requests_per_minute=2)
    
    # Can acquire up to capacity
    assert limiter.acquire() is True
    assert limiter.acquire() is True

    # Third time fails because limit is reached
    assert limiter.acquire() is False


def test_adaptive_backoff_values():
    assert get_adaptive_backoff(0) == 0.0
    
    delay1 = get_adaptive_backoff(1, base_delay=1.0)
    assert 1.0 <= delay1 <= 1.1

    delay2 = get_adaptive_backoff(2, base_delay=1.0)
    assert 2.0 <= delay2 <= 2.2
