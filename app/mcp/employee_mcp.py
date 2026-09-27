"""Employee MCP Tools"""
from typing import Dict, Any
from app.mcp.base import mcp_tool, RiskClassification
from app.services.bigquery_service import bq_service

@mcp_tool(
    name="get_employee_profile",
    description="Retrieve employee corporate profile, limits, and department info",
    risk_classification=RiskClassification.READ_ONLY
)
async def get_employee_profile_tool(employee_id: str, **kwargs) -> Dict[str, Any]:
    emp = await bq_service.get_employee(employee_id)
    if not emp:
        return {"error": f"Employee {employee_id} not found"}
    return emp
