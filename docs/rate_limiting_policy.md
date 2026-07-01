# Client-Side Adaptive Rate Limiting & Backoff (ELUSoC_2026)

## Background
AI agents executing high-frequency tool loops can trigger API rate-limiting blocks or flood target backends. Client-side rate limiting prevents this by pacing calls in the execution wrapper.

## Design
We implement a lightweight thread-safe token-bucket rate limiter that intercepts invocations on monitored agents and delays execution with adaptive backoff when limits are reached.

## Files
- `agentwatch/core/rate_limiter.py` - Token bucket limiter & backoff calculator.
- `tests/test_rate_limiter_policy.py` - Unit test validation.
- `tests/test_rate_limiter_integration.py` - Integration testing with `watch()`.
