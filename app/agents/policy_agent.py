"""Policy Specialist Agent"""
from typing import Dict, Any, List
from app.mcp.policy_mcp import retrieve_policy_clauses_tool
from app.models.schemas import PolicyFinding, Citation
from app.rag.grounding import grounding_verifier

class PolicyAgent:
    def __init__(self, name: str = "policy_agent"):
        self.name = name

    async def investigate(self, transaction_amount: float, merchant_category: str) -> Dict[str, Any]:
        query = f"corporate card single transaction limit {transaction_amount} merchant {merchant_category}"
        res = await retrieve_policy_clauses_tool(query=query, top_k=3)
        data = res.get("data", {})
        
        citations_raw = data.get("citations", [])
        citations = [
            Citation(
                citation_id=c["citation_id"],
                document_name=c["document_name"],
                section_title=c.get("section_title"),
                clause_text=c["clause_text"],
                relevance_score=c.get("relevance_score", 1.0)
            ) for c in citations_raw
        ]
        
        finding = PolicyFinding(
            policy_id="POL-CORP-CARD-2026",
            policy_name="Corporate Card Usage Policy",
            clause_id="3.1",
            is_compliant=(transaction_amount <= 5000.0),
            violation_details=f"Amount ${transaction_amount} exceeds $5,000 single limit" if transaction_amount > 5000.0 else None,
            citations=citations
        )
        
        finding = grounding_verifier.verify_policy_finding(finding, citations)

        return {
            "agent_name": self.name,
            "status": "SUCCESS",
            "policy_finding": finding.model_dump(),
            "citations": [c.model_dump() for c in citations]
        }

policy_agent = PolicyAgent()
