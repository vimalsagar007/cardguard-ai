# CardGuard AI Observability Documentation

## Structured Logging & Latency Monitoring
- **Correlation ID & Trace ID**: Embedded in all HTTP headers, MCP logs, and A2A tasks.
- **Latency Percentiles**: P50 (120ms target), P95 (340ms target), P99 (580ms target).
- **Cost Estimation**: Token consumption and USD cost tracking logged per investigation turn.
