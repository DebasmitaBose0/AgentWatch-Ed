# Custom Adapters Tutorial (ELUSoC_2026)

## Designing an Adapter
If your custom agent framework is not auto-detected by AgentWatch, you can extend the `GenericAdapter` or write your own class.

### 1. Intercepting Calls
To intercept calls, implement wrappers around execution triggers:
```python
def wrap_custom_run(original_run):
    def wrapper(*args, **kwargs):
        # 1. pre-execution safety validation
        # 2. emit session/agent start events
        res = original_run(*args, **kwargs)
        # 3. emit success event
        return res
    return wrapper
```

### 2. Emitting Custom Events
Instantiate `AgentEvent` and publish via `get_event_bus().publish_sync(event)`.
