# CardGuard AI Threat Model & Risk Analysis

## Threat Vectors & Mitigation Strategies

| Threat Vector | Severity | Impact | Mitigation Strategy |
|---|---|---|---|
| **Indirect Prompt Injection** (via RAG documents or merchant notes) | HIGH | Agent manipulation to alter risk score | Input sanitization, strict system instruction boundaries, deterministic decision engine override |
| **Unauthorized High-Risk Tool Execution** | CRITICAL | Unauthorized card block or financial action | MCP `HIGH_RISK_WRITE` decorator requiring explicit `human_authorized=True` flag |
| **LLM Hallucination** (inventing non-existent policies) | MEDIUM | False positive/negative compliance flags | Grounding verifier returning `"Evidence unavailable; unable to verify this claim."` when ungrounded |
| **Replay / Duplicate Transaction Ingestion** | MEDIUM | Duplicate case creation | Transaction idempotency check in `BigQueryService` and `CaseAgent` |
| **Service Outage / Timeout** | MEDIUM | Investigation delay | Exponential backoff, 10s tool timeouts, circuit breakers, fallback responses |
