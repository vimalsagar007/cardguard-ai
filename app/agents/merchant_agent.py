"""Merchant Specialist Agent"""
from typing import Dict, Any
from app.mcp.merchant_mcp import get_merchant_risk_profile_tool
from app.models.schemas import MerchantFinding

class MerchantAgent:
    def __init__(self, name: str = "merchant_agent"):
        self.name = name

    async def investigate(self, merchant_id: str) -> Dict[str, Any]:
        res = await get_merchant_risk_profile_tool(merchant_id=merchant_id)
        merch = res.get("data", {})
        
        finding = MerchantFinding(
            merchant_id=merchant_id,
            merchant_name=merch.get("merchant_name", "Unknown Merchant"),
            risk_score=merch.get("risk_score", 15.0),
            historical_chargeback_rate=merch.get("historical_chargeback_rate", 0.1),
            is_high_risk_mcc=merch.get("is_high_risk_mcc", False),
            is_approved_vendor=merch.get("is_approved_vendor", False),
            notes=f"MCC {merch.get('merchant_category_code')} ({merch.get('mcc_description')}) in {merch.get('country')}"
        )

        return {
            "agent_name": self.name,
            "status": "SUCCESS",
            "merchant_finding": finding.model_dump(),
            "raw_merchant": merch
        }

merchant_agent = MerchantAgent()
