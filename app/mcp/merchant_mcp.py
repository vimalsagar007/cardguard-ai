"""Merchant MCP Tools"""
from typing import Dict, Any
from app.mcp.base import mcp_tool, RiskClassification
from app.services.bigquery_service import bq_service

@mcp_tool(
    name="get_merchant_risk_profile",
    description="Retrieve merchant risk score, MCC code classification, and historical chargeback rates",
    risk_classification=RiskClassification.READ_ONLY
)
async def get_merchant_risk_profile_tool(merchant_id: str, **kwargs) -> Dict[str, Any]:
    merch = await bq_service.get_merchant(merchant_id)
    if not merch:
        return {"error": f"Merchant {merchant_id} not found"}
    return merch
