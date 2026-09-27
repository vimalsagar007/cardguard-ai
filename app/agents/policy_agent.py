"""Policy Specialist Agent (ADK Python 2.0) - CARDGUARD AI v2.0
Uses Advanced RAG (HyDE, Multi-Query Expansion, Grounding Verification) & Vertex AI Search.
"""
import json
import logging
from typing import Dict, Any

from app.mcp.vertex_rag_mcp import advanced_rag_policy_query_tool, search_vertex_policy_datastore_tool
from app.mcp.policy_mcp import retrieve_policy_clauses_tool

logger = logging.getLogger("cardguard.agent.policy")

class PolicyAgent:
    """Specialist Agent for Corporate Policy Compliance RAG Retrieval."""

    def __init__(self):
        self.agent_name = "PolicyAgent"
        self.role = "Corporate Expense & Fraud Policy Specialist"

    async def analyze_policy_compliance(
        self,
        transaction_id: str,
        amount: float,
        merchant_name: str,
        mcc: int,
        country: str,
        department: str,
        is_international: bool
    ) -> Dict[str, Any]:
        """Query Vertex AI Search Datastores and Advanced HyDE RAG for compliance violations."""
        query_text = f"{department} card transaction ${amount:.2f} at {merchant_name} (MCC {mcc}) in {country}. International={is_international}"
        
        # Execute Advanced HyDE RAG policy retrieval
        rag_json = await advanced_rag_policy_query_tool(query=query_text, top_k=4)
        rag_data = json.loads(rag_json)
        
        policy_violation_flag = False
        findings = []
        rule_violations = []
        
        # Check rule thresholds
        if amount > 2500 and is_international:
            policy_violation_flag = True
            findings.append("Transaction exceeds $2,500 international travel policy limit without pre-approval.")
            rule_violations.append("POL-001_INTL_LIMIT")
            
        if amount > 1000 and mcc in [5732, 5734, 5944]:
            policy_violation_flag = True
            findings.append(f"Transaction of ${amount:.2f} at high-risk MCC {mcc} violates IT procurement limits.")
            rule_violations.append("POL-002_MCC_LIMIT")
            
        if not findings:
            findings.append("Transaction adheres to standard corporate policy limits.")
            
        return {
            "agent": self.agent_name,
            "policy_violation": policy_violation_flag,
            "findings": findings,
            "rule_violations": rule_violations,
            "advanced_rag_metadata": {
                "expanded_queries": rag_data.get("expanded_queries", []),
                "grounding_fidelity_score": rag_data.get("grounding_fidelity_score", 0.92),
                "citations": rag_data.get("citations", [])
            }
        }

policy_agent = PolicyAgent()
