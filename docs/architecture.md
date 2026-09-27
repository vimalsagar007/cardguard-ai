# CardGuard AI Architecture Documentation

## Overview
CardGuard AI is an enterprise corporate card fraud investigation and decision intelligence platform built using Google-native AI technology, ADK (Agent Development Kit), Gemini 3.8 models, Model Context Protocol (MCP), Agent-to-Agent (A2A) protocol, BigQuery, and Pub/Sub.

## System Components
1. **Analyst Dashboard**: Modern Web UI displaying real-time fraud alerts, evidence graphs, agent collaboration timelines, and human approval gates.
2. **FastAPI Gateway**: Enterprise REST API exposing investigation, case management, approval, and metrics endpoints.
3. **CardGuard Supervisor Agent**: ADK Python orchestrator handling task decomposition, parallel execution, evidence validation, and approval gating.
4. **Specialist Agents**:
   - `fraud_investigation_agent`: Anomaly detection, velocity scoring, amount checks.
   - `policy_agent`: Policy RAG vector search, citation verification.
   - `merchant_agent`: MCC category risk scoring, chargeback profiling.
   - `employee_agent`: Baseline spending analysis, corporate card limit checks.
   - `case_agent`: Case timeline management and reviewer assignment.
   - `decision_agent`: Deterministic decision engine wrapper.
5. **Model Context Protocol (MCP)**: Tool abstraction with circuit breakers, retries, and strict `HIGH_RISK_WRITE` human approval enforcement.
6. **Grounding Pipeline**: Vector + BM25 hybrid policy retrieval with citation verification and anti-hallucination safeguards.
