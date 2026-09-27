# CardGuard AI Model Context Protocol (MCP)

## MCP Tool Classifications
- `READ_ONLY`: `get_transaction`, `query_card_velocity`, `get_employee_profile`, `get_merchant_risk_profile`, `retrieve_policy_clauses`, `get_case_details`.
- `LOW_RISK_WRITE`: `update_case_status`, `add_evidence`.
- `HIGH_RISK_WRITE`: `execute_card_block_action`. Requires explicit `human_authorized=True` flag and analyst ID.
