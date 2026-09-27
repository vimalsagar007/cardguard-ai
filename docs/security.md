# CardGuard AI Security Architecture

## Principles
1. **Least Privilege & Workload Identity**: All GCP service interactions operate under dedicated service accounts with scoped IAM permissions.
2. **LLM Non-Autonomy for Irreversible Writes**: LLM agents generate recommendations but are strictly prevented from performing high-risk financial actions (e.g. card blocks, merchant bans) without deterministic rule validation and human approval.
3. **Prompt Injection Defense**: All user inputs and retrieved RAG context pass through prompt injection regex filters and semantic guardrails.
4. **Secret Manager**: Secrets, tokens, and API credentials are stored in Google Cloud Secret Manager.
5. **No PII/Cardholder Data**: Card numbers are masked (`CARD-xxxx`), and only synthetic financial data is processed.
