"""Case Management Specialist Agent"""
import uuid
from datetime import datetime
from typing import Dict, Any
from app.mcp.case_mcp import update_case_status_tool, get_case_details_tool
from app.models.schemas import Case, RiskLevel, DecisionType

class CaseAgent:
    def __init__(self, name: str = "case_agent"):
        self.name = name

    async def create_or_update_case(
        self,
        transaction_id: str,
        risk_level: RiskLevel,
        risk_score: float,
        decision: DecisionType,
        summary: str
    ) -> Dict[str, Any]:
        case_id = f"CASE-{transaction_id.replace('TXN-', '')}"
        
        status = "PENDING_APPROVAL" if decision == DecisionType.BLOCK_PENDING_APPROVAL else "CLOSED"
        if decision == DecisionType.ESCALATE:
            status = "IN_INVESTIGATION"
            
        res = await update_case_status_tool(
            case_id=case_id,
            status=status,
            timeline_event=f"Case evaluated by CardGuard AI: Decision={decision.value}, Score={risk_score:.1f}",
            actor=self.name
        )
        
        return {
            "agent_name": self.name,
            "status": "SUCCESS",
            "case_id": case_id,
            "case_status": status
        }

case_agent = CaseAgent()
