"""Decision MCP Tools"""
from typing import Dict, Any
from app.mcp.base import mcp_tool, RiskClassification

@mcp_tool(
    name="execute_card_block_action",
    description="Execute irreversible corporate card block or merchant ban. Requires explicit human approval.",
    risk_classification=RiskClassification.HIGH_RISK_WRITE
)
async def execute_card_block_action_tool(
    card_id: str,
    action: str,
    human_authorized: bool = False,
    approver_id: str = None,
    **kwargs
) -> Dict[str, Any]:
    # Will be blocked by mcp_tool decorator if human_authorized is False
    return {
        "status": "EXECUTED",
        "card_id": card_id,
        "action": action,
        "approver_id": approver_id,
        "message": f"Action {action} successfully executed for card {card_id} with human authorization from {approver_id}."
    }
