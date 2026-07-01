"""
ELUSoC_2026 - Semantic cache for repeated LLM subtasks.
Provides semantic caching mechanisms to avoid duplicate model calls, reducing costs and latency.
"""

from __future__ import annotations

import logging
import re
import threading
from typing import Any

logger = logging.getLogger(__name__)


class SemanticCache:
    """A thread-safe semantic cache for LLM queries and responses.
    
    Uses a normalized token similarity to match semantic overlap
    without requiring heavy external machine learning dependencies.
    """

    def __init__(self, threshold: float = 0.75) -> None:
        self.threshold = threshold
        self._cache: list[dict[str, Any]] = []
        self._lock = threading.Lock()
        self.hits = 0
        self.misses = 0
        self.tokens_saved = 0

    def _tokenize(self, text: str) -> set[str]:
        """Convert text into normalized set of lowercase words/tokens."""
        text = text.lower()
        # Clean common contractions and punctuation
        text = text.replace("'s", "").replace("n't", " not")
        words = re.findall(r"\b\w{3,}\b", text)
        return set(words)

    def _similarity(self, tokens1: set[str], tokens2: set[str]) -> float:
        """Calculate Jaccard similarity coefficient between two sets of tokens."""
        if not tokens1 or not tokens2:
            return 0.0
        intersection = tokens1.intersection(tokens2)
        union = tokens1.union(tokens2)
        return len(intersection) / len(union)

    def lookup(self, query: str) -> tuple[Any | None, float]:
        """Look up a query in the cache. Returns (cached_response, similarity_score)."""
        if not query or not isinstance(query, str):
            return None, 0.0

        # Extract only the actual query part if it's formatted as 'method_name:args:kwargs'
        actual_query = query
        if ":" in query:
            parts = query.split(":", 1)
            actual_query = parts[1]

        query_tokens = self._tokenize(actual_query)
        if not query_tokens:
            return None, 0.0

        best_score = 0.0
        best_response = None

        with self._lock:
            for entry in self._cache:
                # Compare the actual query text stored
                entry_actual = entry["query"]
                if ":" in entry_actual:
                    entry_actual = entry_actual.split(":", 1)[1]
                
                entry_tokens = self._tokenize(entry_actual)
                score = self._similarity(query_tokens, entry_tokens)
                if score > best_score:
                    best_score = score
                    best_response = entry["response"]

        if best_score >= self.threshold:
            self.hits += 1
            logger.info("Semantic cache hit! Score: %.2f", best_score)
            return best_response, best_score

        self.misses += 1
        return None, best_score

    def store(self, query: str, response: Any, token_count: int = 0) -> None:
        """Store a query-response pair in the semantic cache."""
        if not query or not isinstance(query, str):
            return

        query_tokens = self._tokenize(query)
        if not query_tokens:
            return

        with self._lock:
            # Check if this query is already stored to avoid duplicate entries
            for entry in self._cache:
                if entry["query"] == query:
                    entry["response"] = response
                    entry["token_count"] = token_count
                    return
            
            self._cache.append({
                "query": query,
                "tokens": query_tokens,
                "response": response,
                "token_count": token_count
            })
            logger.debug("Stored response in semantic cache (total entries: %d)", len(self._cache))

    def clear(self) -> None:
        """Clear all entries in the cache."""
        with self._lock:
            self._cache.clear()
            self.hits = 0
            self.misses = 0
            self.tokens_saved = 0

    def get_stats(self) -> dict[str, int | float]:
        """Return cache usage statistics."""
        with self._lock:
            total = self.hits + self.misses
            hit_rate = (self.hits / total) if total > 0 else 0.0
            return {
                "hits": self.hits,
                "misses": self.misses,
                "hit_rate": hit_rate,
                "tokens_saved": self.tokens_saved,
                "entries": len(self._cache)
            }
