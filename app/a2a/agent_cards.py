"""Agent Cards for CardGuard AI A2A Protocol"""
from typing import Dict, Any, List

def get_agent_cards() -> Dict[str, Dict[str, Any]]:
    return {
        "supervisor_agent": {
            "name": "supervisor_agent",
            "description": "Orchestrates corporate card fraud investigations, parallelizes agent sub-tasks, and validates evidence.",
            "version": "1.0.0",
            "capabilities": ["investigation_orchestration", "evidence_aggregation", "approval_gating"],
            "endpoint": "/a2a/supervisor_agent"
        },
        "fraud_investigation_agent": {
            "name": "fraud_investigation_agent",
            "description": "Analyzes card velocity, amount anomalies, geographic jumps, and generates fraud signals.",
            "version": "1.0.0",
            "capabilities": ["velocity_analysis", "amount_anomaly_detection", "geo_jump_detection"],
            "endpoint": "/a2a/fraud_investigation_agent"
        },
        "policy_agent": {
            "name": "policy_agent",
            "description": "Queries corporate policy RAG vector store and retrieves grounded policy citations.",
            "version": "1.0.0",
            "capabilities": ["policy_rag_retrieval", "citation_verification", "grounding_validation"],
            "endpoint": "/a2a/policy_agent"
        },
        "merchant_agent": {
            "name": "merchant_agent",
            "description": "Retrieves merchant category code risk profiles and historical chargeback rates.",
            "version": "1.0.0",
            "capabilities": ["merchant_risk_profiling", "mcc_classification"],
            "endpoint": "/a2a/merchant_agent"
        },
        "employee_agent": {
            "name": "employee_agent",
            "description": "Fetches employee card limits, spending baselines, and historical fraud records.",
            "version": "1.0.0",
            "capabilities": ["employee_baseline_analysis", "card_limit_lookup"],
            "endpoint": "/a2a/employee_agent"
        },
        "case_agent": {
            "name": "case_agent",
            "description": "Creates and manages investigation case records, audit trails, and reviewer assignments.",
            "version": "1.0.0",
            "capabilities": ["case_management", "audit_timeline_logging"],
            "endpoint": "/a2a/case_agent"
        },
        "decision_agent": {
            "name": "decision_agent",
            "description": "Evaluates deterministic risk rules and produces structured decision recommendations.",
            "version": "1.0.0",
            "capabilities": ["deterministic_risk_scoring", "human_approval_triggering"],
            "endpoint": "/a2a/decision_agent"
        }
    }
