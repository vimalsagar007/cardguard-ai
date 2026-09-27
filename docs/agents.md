# CardGuard AI Agents Specification

## Agent Roster & Responsibilities
- `supervisor_agent`: Master orchestrator coordinating task decomposition and parallel execution.
- `fraud_investigation_agent`: Anomaly detection, velocity scoring, amount checks.
- `policy_agent`: RAG policy search and citation verification.
- `merchant_agent`: MCC category risk scoring and chargeback rate calculation.
- `employee_agent`: Baseline spending analysis and single transaction limit checks.
- `case_agent`: Case state management and audit timeline logging.
- `decision_agent`: Deterministic risk engine score calculation.
