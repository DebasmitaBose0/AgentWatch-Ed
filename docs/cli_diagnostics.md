# CLI Environment Diagnostics Tool (ELUSoC_2026)

## Background
AgentWatch orchestrates safety/reliability across various agent frameworks. Since these libraries run on fast-moving versions, package mismatches are common.

## Design
We provide a dedicated CLI command `agentwatch diagnose` that scans active packages (Pydantic, FastAPI, Celery, SQLAlchemy), reports version details, and highlights compatibility conflicts.

## Usage
Run:
```bash
agentwatch diagnose
```
This lists package states and outputs warnings for suboptimal configurations.
