"""Transaction MCP Tools"""
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from app.mcp.base import mcp_tool, RiskClassification
from app.services.bigquery_service import bq_service

class GetTransactionInput(BaseModel):
    transaction_id: str = Field(description="Transaction ID")

@mcp_tool(
    name="get_transaction",
    description="Retrieve transaction details by transaction ID from BigQuery storage",
    risk_classification=RiskClassification.READ_ONLY
)
async def get_transaction_tool(transaction_id: str, **kwargs) -> Dict[str, Any]:
    tx = await bq_service.get_transaction(transaction_id)
    if not tx:
        return {"error": f"Transaction {transaction_id} not found"}
    return tx

@mcp_tool(
    name="query_card_velocity",
    description="Query historical transaction velocity for a corporate card ID",
    risk_classification=RiskClassification.READ_ONLY
)
async def query_card_velocity_tool(card_id: str, minutes_window: int = 60, **kwargs) -> Dict[str, Any]:
    txs = await bq_service.query_card_velocity(card_id, minutes_window)
    return {
        "card_id": card_id,
        "window_minutes": minutes_window,
        "transaction_count": len(txs),
        "recent_transactions": txs
    }
