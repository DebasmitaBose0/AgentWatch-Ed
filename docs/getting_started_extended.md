# Extended Getting Started Guide (ELUSoC_2026)

## Setup Configuration
Create a `.env` file in the root folder:
```env
AGENTWATCH_ENV=development
DATABASE_URL=sqlite:///agentwatch.db
REDIS_URL=redis://localhost:6379/0
```

## First Instrumentation
Create a simple python script to verify watcher:
```python
from agentwatch import watch

class MySimpleAgent:
    def run(self, query: str) -> str:
        return f"Processed: {query}"

agent = watch(MySimpleAgent())
agent.run("Scan safety protocols.")
```
Ensure your logs indicate `SESSION_START` and `AGENT_START` triggers.
