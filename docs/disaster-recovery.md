# CardGuard AI Disaster Recovery Plan

## Failover & Resiliency
- **Circuit Breakers**: MCP tools enter open circuit state after 3 consecutive failures.
- **Data Persistence**: In-memory datasets sync state with BigQuery and Cloud Storage.
- **RTO & RPO**: Recovery Time Objective (RTO) < 5 minutes; Recovery Point Objective (RPO) < 1 minute.
