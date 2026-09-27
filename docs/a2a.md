# CardGuard AI Agent-to-Agent (A2A) Protocol

## A2A Architecture
- **Agent Cards**: Standard JSON agent manifests exposed via `/.well-known/agent-card.json`.
- **Task Contracts**: Strongly typed Pydantic task request/response models.
- **Trace Propagation**: All A2A tasks carry `correlation_id` and `trace_id` headers.
