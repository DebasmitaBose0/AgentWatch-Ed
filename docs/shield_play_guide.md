# Interactive Safety Playground (ELUSoC_2026)

## Background
Developers need a fast way to verify how their agent security/safety policies handle dangerous prompts, command injections, and destructive commands before running them in production.

## Design
We expose an interactive console utility through the CLI: `agentwatch safety play`. This starts a loop where developers can type any text and see the Safety Engine block verdict.

## Usage
Run:
```bash
agentwatch safety play
```
Example:
```bash
SafetyCheck > rm -rf /etc
❌ BLOCKED - Match reasons: Destructive command check failed
```
