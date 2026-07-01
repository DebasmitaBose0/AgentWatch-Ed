"""
ELUSoC_2026 - Client-Side Rate Limiter & Adaptive Backoff.
Enforces client-side rate limits and backoff strategies on wrapped agent calls.
"""

from __future__ import annotations

import logging
import threading
import time
from typing import Any

logger = logging.getLogger(__name__)


class ClientRateLimiter:
    """Token-bucket rate limiter for client-side agent calls."""

    def __init__(self, requests_per_minute: int = 60) -> None:
        self.capacity = requests_per_minute
        self.tokens = float(requests_per_minute)
        self.fill_rate = requests_per_minute / 60.0
        self.last_fill = time.monotonic()
        self._lock = threading.Lock()

    def _consume(self) -> bool:
        with self._lock:
            now = time.monotonic()
            elapsed = now - self.last_fill
            self.tokens = min(self.capacity, self.tokens + elapsed * self.fill_rate)
            self.last_fill = now

            if self.tokens >= 1.0:
                self.tokens -= 1.0
                return True
            return False

    def acquire(self) -> bool:
        """Acquire a token, returning True if successful."""
        return self._consume()


def get_adaptive_backoff(retry_count: int, base_delay: float = 1.0, max_delay: float = 60.0) -> float:
    """Calculate exponential backoff delay with jitter."""
    import random
    
    if retry_count <= 0:
        return 0.0
    delay = min(max_delay, base_delay * (2 ** (retry_count - 1)))
    jitter = random.uniform(0, 0.1 * delay)  # nosec B311 — non-cryptographic jitter
    return delay + jitter
