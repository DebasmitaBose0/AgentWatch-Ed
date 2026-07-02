# AgentWatch API Reference

This document describes every public REST API endpoint exposed by the AgentWatch API server and every method/class in the public Python SDK.

---

## Base URL

All REST endpoints are served from the FastAPI application under `/api/v1`.  
In development the default URL is `http://localhost:8000/api/v1`.  
The frontend proxy defaults to `/api/v1`; override with `NEXT_PUBLIC_API_URL`.

### Authentication

Most endpoints require an API key passed via the `X-API-Key` header.  
Keys are generated per tenant (see [Tenant Management](#tenant-management)).

---

## REST API Endpoints

### System

#### `GET /api/v1/system/status`

Returns infrastructure health and component status.

- **Auth**: None
- **Response**: `{"status": "ok", "components": {...}}`

---

#### `GET /health`

Quick health check (alias for system status).

- **Auth**: None
- **Response**: `{"status": "ok"}`

---

#### `GET /metrics`

Prometheus-formatted metrics endpoint.

- **Auth**: None
- **Response**: Plain text Prometheus metrics

---

### Sessions

#### `GET /api/v1/sessions`

List sessions with optional filters.

- **Auth**: API key
- **Query params**:
  - `limit` (int, default: 50) — max sessions to return
  - `framework` (str, optional) — filter by framework label
  - `status` (str, optional) — filter by execution status
  - `since_hours` (int, optional) — only sessions updated in last N hours
- **Response**: `{"sessions": [...], "total": int}`

---

#### `POST /api/v1/sessions`

Create a new session.

- **Auth**: API key
- **Body**: `{"session_id": str, "agent_id": str, "framework": str, ...}`
- **Response**: `{"session_id": str, "created_at": str}`

---

#### `GET /api/v1/sessions/{session_id}`

Get a single session by ID.

- **Auth**: API key
- **Response**: Full session object

---

#### `DELETE /api/v1/sessions/prune`

Delete old sessions.

- **Auth**: API key
- **Query params**: `older_than_hours` (int), `dry_run` (bool, default: false)
- **Response**: `{"deleted": int, "dry_run": bool}`

---

#### `GET /api/v1/sessions/{session_id}/events`

Get all events for a session.

- **Auth**: API key
- **Response**: `{"events": [AgentEvent, ...], "total": int}`

---

#### `GET /api/v1/sessions/{session_id}/trace`

Get the full trace (events + metadata) for a session.

- **Auth**: API key
- **Response**: Full trace dictionary

---

#### `GET /api/v1/sessions/{session_id}/confidence`

Get confidence scoring for a session.

- **Auth**: API key
- **Response**: `{"overall_score": float, "goal_alignment": float, "consistency_score": float, "anomaly_flags": [str], "explanation": str}`

---

#### `GET /api/v1/sessions/{session_id}/reasoning`

Get the reasoning audit for a session.

- **Auth**: API key
- **Response**: Reasoning audit report

---

#### `GET /api/v1/sessions/{session_id}/cost`

Get cost and token usage for a session.

- **Auth**: API key
- **Response**: `{"total_tokens": int, "estimated_cost_usd": float, ...}`

---

#### `GET /api/v1/sessions/{session_id}/replay`

Replay a session step by step.

- **Auth**: API key
- **Response**: Replay data with ordered events

---

#### `POST /api/v1/sessions/{session_id}/simulate`

Run a counterfactual simulation against a session.

- **Auth**: API key
- **Body**: `{"scenario": CounterfactualScenario}`
- **Response**: Simulation result

---

#### `GET /api/v1/sessions/{session_id}/checkpoints`

List rollback checkpoints for a session.

- **Auth**: API key
- **Response**: `{"checkpoints": [Checkpoint, ...]}`

---

#### `POST /api/v1/sessions/{session_id}/rollback`

Trigger a rollback to a specific checkpoint.

- **Auth**: API key
- **Body**: `{"checkpoint_id": str, "restore_filesystem": bool, "restore_git": bool}`
- **Response**: `{"status": str, "rolled_back_files": [str], ...}`

---

### Events

#### `POST /api/v1/events`

Ingest a single event.

- **Auth**: API key
- **Body**: Full `AgentEvent` JSON payload
- **Response**: `{"accepted": bool, "event_id": str}`

---

### Safety

#### `GET /api/v1/safety/policy`

Get the current safety policy.

- **Auth**: API key
- **Response**: `{"version": str, "blocked_commands": [str], "risk_thresholds": {...}}`

---

#### `PUT /api/v1/safety/policy`

Update the safety policy.

- **Auth**: API key (requires `policy:write` permission)
- **Body**: Safety policy JSON
- **Response**: Updated policy

---

#### `GET /api/v1/safety/blocked`

List blocked events.

- **Auth**: API key
- **Response**: `{"blocked_events": [BlockedEvent, ...]}`

---

#### `POST /api/v1/safety/check`

Test a command or action against the safety policy without executing it.

- **Auth**: API key
- **Body**: `{"command": str, "context": {...}}`
- **Response**: `{"safe": bool, "risk_level": str, "reason": str}`

---

### Dashboard

#### `GET /api/v1/dashboard/summary`

Aggregate statistics for the dashboard.

- **Auth**: API key
- **Response**: `{"total_sessions": int, "total_events": int, "active_sessions": int, "blocked_count": int, ...}`

---

#### `GET /api/v1/dashboard/top`

Top active sessions.

- **Auth**: API key
- **Response**: `{"sessions": [SessionSummary, ...]}`

---

### Governance

#### `GET /api/v1/governance/compliance-report`

Generate a compliance report (SOC2, GDPR, HIPAA, etc.).

- **Auth**: API key (requires `governance:read`)
- **Response**: Compliance report JSON

---

#### `GET /api/v1/governance/eu-ai-act-report`

Generate an EU AI Act Article 15 conformity report.

- **Auth**: API key (requires `governance:read`)
- **Response**: EU AI Act report JSON

---

#### `POST /api/v1/entitlement/usage`

Report entitlement usage metering data.

- **Auth**: API key
- **Body**: Entitlement usage payload
- **Response**: `{"recorded": bool}`

---

### Tenant Management (Cloud Mode)

*These endpoints are only available when `AGENTWATCH_CLOUD_MODE=true`.*

#### `POST /api/v1/tenants`

Create a new tenant.

- **Auth**: Master API key
- **Body**: `{"name": str, "plan": str, ...}`
- **Response**: Created tenant object

---

#### `GET /api/v1/tenants`

List all tenants.

- **Auth**: Master API key
- **Response**: `{"tenants": [Tenant, ...]}`

---

#### `GET /api/v1/tenants/{tenant_id}`

Get a single tenant by ID.

- **Auth**: Master API key
- **Response**: Full tenant object

---

#### `POST /api/v1/tenants/{tenant_id}/api-keys`

Create a new API key for a tenant.

- **Auth**: Master API key
- **Body**: `{"name": str, "scopes": [str]}`
- **Response**: `{"key_id": str, "raw_key": str}` (raw key shown once)

---

#### `GET /api/v1/tenants/{tenant_id}/api-keys`

List API keys for a tenant.

- **Auth**: Master API key
- **Response**: `{"api_keys": [ApiKey, ...]}` (hashes only, no raw keys)

---

#### `DELETE /api/v1/tenants/{tenant_id}/api-keys/{key_id}`

Revoke an API key.

- **Auth**: Master API key
- **Response**: `{"revoked": bool}`

---

#### `GET /api/v1/tenants/{tenant_id}/usage`

Get usage metrics for a tenant.

- **Auth**: Master API key
- **Response**: `{"tokens_used": int, "requests_count": int, "usd_cost": float, ...}`

---

### Ingestion

#### `GET /api/v1/ingestion/metrics`

Get ingestion pipeline metrics.

- **Auth**: API key
- **Response**: Ingestion metrics per tenant

---

### Demo

#### `POST /api/v1/demo/seed`

Seed the database with demo data.

- **Auth**: API key
- **Response**: `{"seeded": bool, "sessions_created": int}`

---

### WebSocket

#### `WS /ws/events`

Real-time event stream.

- **Auth**: API key passed as `X-API-Key` header or query param `api_key`
- **Protocol**: Server pushes `AgentEvent` JSON messages as they are published to the EventBus
- **Close codes**: `4001` if authentication fails

---

## Python SDK

The public API surface is imported directly from the `agentwatch` package:

```python
import agentwatch
```

### `watch(target, *, api_key=None, base_url=None, ...)`

Attach AgentWatch monitoring to any supported framework object (LangChain chain, CrewAI crew, AutoGPT instance, etc.).

**Parameters**:
- `target` — A framework object or a dict/list of objects to instrument
- `api_key` (str, optional) — API key for cloud mode
- `base_url` (str, optional) — API base URL (default: `/api/v1`)
- `session_id` (str, optional) — explicit session ID; auto-generated if omitted
- `extra_metadata` (dict, optional) — custom metadata attached to all events

**Returns**: An `AgentSession` or list of `AgentSession` objects.

---

### `detect_framework(target)`

Auto-detect which AI agent framework a given object belongs to.

**Parameters**:
- `target` — Any Python object

**Returns**: `AgentFramework` enum member or `None`.

---

### `detect_framework_label(target)`

Return a human-readable framework label for a target object.

**Parameters**:
- `target` — Any Python object

**Returns**: `str` (e.g. `"langchain"`, `"crewai"`, `"autogen"`) or `"unknown"`.

---

### `GenericAdapter`

Base class for implementing custom framework adapters. Subclass and implement `wrap_methods()`.

```python
from agentwatch import GenericAdapter

class MyFrameworkAdapter(GenericAdapter):
    def wrap_methods(self, target):
        # intercept methods, emit AgentEvent instances
        pass
```

---

### `AgentWatchBlockedError`

Exception raised when the Safety Engine blocks an action. Contains the blocking reason and risk level.

```python
from agentwatch import AgentWatchBlockedError

try:
    result = agent.run(task)
except AgentWatchBlockedError as e:
    print(f"Blocked: {e}")
```

---

## Data Models

### `AgentEvent`

The universal event schema. Every framework adapter normalizes framework-specific execution artifacts into this model.

| Field | Type | Description |
|---|---|---|
| `session_id` | `str` | Session identifier |
| `agent_id` | `str` | Agent identifier |
| `event_type` | `EventType` | Type of event (TOOL_CALL, LLM_CALL, AGENT_START, etc.) |
| `timestamp` | `str` (ISO 8601) | When the event occurred |
| `tool_call` | `ToolCallData \| None` | Tool invocation details |
| `tool_result` | `ToolResultData \| None` | Tool execution result |
| `safety` | `SafetyCheckData \| None` | Safety check result |
| `token_usage` | `TokenUsage \| None` | Token consumption |
| `status` | `ExecutionStatus` | Execution status (SUCCESS, FAILURE, BLOCKED) |
| `is_blocked` | `bool` | Whether the action was blocked |
| `metadata` | `dict` | Arbitrary metadata |

### `ConfidenceData`

| Field | Type | Description |
|---|---|---|
| `overall_score` | `float` | 0.0 (very anomalous) — 1.0 (healthy) |
| `goal_alignment` | `float` | 0.0 — 1.0 |
| `consistency_score` | `float` | 0.0 — 1.0 |
| `anomaly_flags` | `list[str]` | Detected anomaly types |
| `explanation` | `str` | Human-readable explanation |

---

## Rate Limiting

- **Read endpoints**: 1,000 requests per 60 s window per IP
- **Write endpoints**: 200 requests per 60 s window per IP
- **Per-tenant ingestion**: Configurable via `TenantConfig.ingestion_rate_limit`

Headers `X-RateLimit-Limit`, `X-RateLimit-Remaining`, and `X-RateLimit-Reset` are set on every response.

---

## Error Responses

All errors follow the format:

```json
{
    "detail": "Human-readable error message"
}
```

HTTP status codes:
- `400` — Bad request (invalid input)
- `401` — Missing or invalid API key
- `403` — Insufficient permissions
- `404` — Resource not found
- `429` — Rate limit exceeded
- `500` — Internal server error
