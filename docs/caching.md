# Semantic Caching for AI Agents (ELUSoC_2026)

## Background
AI Agent subtasks and tool calls often involve duplicate or highly similar queries to LLMs or deterministic backends. Directly executing these subtasks every time results in:
1. Increased execution costs (tokens).
2. Unnecessary execution latency.
3. Waste of rate limits and resources.

## Solution
AgentWatch incorporates an optional, highly configurable **Token-Aware Semantic Cache** layer directly into the `watch()` wrapper. When an agent calls a subtask or invokes a tool, the request is evaluated against historical queries. If a semantic match is found above the set threshold (default: 0.75), the cached response is returned immediately.

## Configuration
The cache runs automatically within the generic wrapper:
```python
from agentwatch import watch

# Initialize watcher with auto semantic caching
agent = watch(my_agent)
```
The semantic threshold and other params can be fine-tuned inside `agentwatch/core/cache.py`.
