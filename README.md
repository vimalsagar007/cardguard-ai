# CARDGUARD AI: Enterprise Corporate Card Fraud Investigation & Decision Intelligence Platform

CardGuard AI is an enterprise-grade reference architecture for real-time corporate card fraud investigation, evidence-backed multi-agent decision intelligence, and automated compliance policy verification. Built natively on Google Cloud and Gemini AI technologies, CardGuard AI combines autonomous agent collaboration with deterministic decision rules and human-in-the-loop (HITL) approval controls.
---

## 🌟 Key Architecture & Capabilities

- **Google-Native Agent Framework**: Built with Google Agent Development Kit (ADK) Python 2.0 and Gemini 3.8 models.
- **Multi-Agent Orchestration**: Specialized sub-agents (`fraud`, `policy`, `merchant`, `employee`, `case`, `decision`) coordinated by a `supervisor_agent`.
- **Model Context Protocol (MCP)**: Production MCP servers (`transaction`, `employee`, `merchant`, `policy`, `case`, `decision`) with Pydantic validation, explicit risk classifications (`READ_ONLY`, `LOW_RISK_WRITE`, `HIGH_RISK_WRITE`), rate limiting, circuit breakers, and audit logging.
- **Agent-to-Agent (A2A) Protocol**: Standards-compliant agent-to-agent collaboration via Agent Cards (`/.well-known/agent-card.json`) and typed task contracts.
- **Deterministic Decision Engine**: Non-LLM deterministic rules engine computing transparent risk scores and enforcing mandatory human approval before high-risk actions.
- **Policy RAG & Grounding Pipeline**: Vector + BM25 hybrid search over synthetic corporate card and travel policies with temporal policy versioning and citation verification.
- **Analyst Dashboard**: Modern enterprise web dashboard with real-time investigation metrics, evidence graphs, chronological timelines, and HITL approval workflow.
- **Enterprise Security & Observability**: Prompt injection defense, secret management, Cloud Trace, BigQuery audit events, and automated AI evaluation metrics.

---

## 📁 Repository Structure

```
cardguard-ai/
├── app/                  # Application source code
│   ├── agents/           # ADK Python multi-agent definitions
│   ├── api/              # FastAPI endpoints & gateway
│   ├── a2a/              # Agent-to-Agent protocol interfaces
│   ├── config/           # Application configuration & Pydantic settings
│   ├── decision_engine/  # Deterministic rule engine & scoring
│   ├── mcp/              # Model Context Protocol servers & tools
│   ├── models/           # Shared Pydantic data schemas
│   ├── rag/              # Vector search & policy grounding pipeline
│   ├── services/         # BigQuery, Pub/Sub, Storage & Cloud services
│   └── tools/            # Custom agent tools & helper functions
├── data/                 # Synthetic datasets & policy knowledge PDFs
├── docs/                 # Architecture, security, & API documentation
├── frontend/             # Analyst Dashboard UI (React/Vite)
├── scripts/              # Synthetic data generator & load test scripts
├── terraform/            # Multi-environment Infrastructure as Code (dev/test/prod)
└── tests/                # Unit, integration, security, adversarial & eval tests
```

---

## 🚀 Quick Start & Local Development

1. **Configure Environment**:
   ```bash
   cp .env.example .env
   ```

2. **Install Dependencies**:
   ```bash
   pip install -e .[dev]
   ```

3. **Generate Synthetic Data**:
   ```bash
   python scripts/generate_synthetic_data.py
   ```

4. **Run FastAPI Service**:
   ```bash
   uvicorn app.api.main:app --reload
   ```

5. **Run Analyst Dashboard**:
   ```bash
   cd frontend && npm install && npm run dev
   ```

---

## 📊 Evaluation & Verification

To run the complete test and evaluation suite:
```bash
pytest tests/
python scripts/run_eval.py
```
