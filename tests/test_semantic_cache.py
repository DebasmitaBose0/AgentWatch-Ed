"""Unit tests for the SemanticCache implementation."""

from __future__ import annotations

import time
import pytest
from agentwatch.core.cache import SemanticCache


def test_semantic_cache_basic_ops():
    cache = SemanticCache(threshold=0.8)

    # Miss path
    res, score = cache.lookup("What is the capital of France?")
    assert res is None
    assert cache.misses == 1
    assert cache.hits == 0

    # Store
    cache.store("What is the capital of France?", "Paris", token_count=10)

    # Exact Hit path
    res, score = cache.lookup("What is the capital of France?")
    assert res == "Paris"
    assert score == 1.0
    assert cache.hits == 1

    # Semantic Hit path (fuzzy match)
    res, score = cache.lookup("What's the capital of France?")
    assert res == "Paris"
    assert score >= 0.8
    assert cache.hits == 2


def test_semantic_cache_miss_threshold():
    cache = SemanticCache(threshold=0.9)
    cache.store("Identify the main security bugs in this server configuration.", "Config bypass found.")

    res, score = cache.lookup("What are the bugs in this file?")
    assert res is None  # Below threshold
    assert cache.misses == 1
