"""Case MCP Tools"""
from typing import Dict, Any
from app.mcp.base import mcp_tool, RiskClassification
from app.services.bigquery_service import bq_service

@mcp_tool(
    name="get_case_details",
    description="Retrieve fraud investigation case state and timeline",
    risk_classification=RiskClassification.READ_ONLY
)
async def get_case_details_tool(case_id: str, **kwargs) -> Dict[str, Any]:
    case_data = await bq_service.get_case(case_id)
    if not case_data:
        return {"error": f"Case {case_id} not found"}
    return case_data

@mcp_tool(
    name="update_case_status",
    description="Update investigation case state, append timeline events, or reassign reviewer",
    risk_classification=RiskClassification.LOW_RISK_WRITE
)
async def update_case_status_tool(case_id: str, status: str, timeline_event: str = None, **kwargs) -> Dict[str, Any]:
    case_data = await bq_service.get_case(case_id)
    if not case_data:
        case_data = {
            "case_id": case_id,
            "status": status,
            "timeline": []
        }
    case_data["status"] = status
    if timeline_event:
        case_data.setdefault("timeline", []).append({
            "event": timeline_event,
            "actor": kwargs.get("actor", "case_agent")
        })
    await bq_service.save_case(case_data)
    return {"status": "SUCCESS", "case_id": case_id, "updated_status": status}
