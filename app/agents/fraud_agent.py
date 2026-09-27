"""Fraud Investigation Specialist Agent"""
from typing import Dict, Any, List
from app.mcp.transaction_mcp import get_transaction_tool, query_card_velocity_tool
from app.models.schemas import FraudSignal, RiskLevel

class FraudInvestigationAgent:
    def __init__(self, name: str = "fraud_investigation_agent"):
        self.name = name

    async def investigate(self, transaction_id: str, card_id: str) -> Dict[str, Any]:
        # 1. Fetch transaction
        tx_res = await get_transaction_tool(transaction_id=transaction_id)
        tx = tx_res.get("data", {})
        
        # 2. Fetch velocity
        vel_res = await query_card_velocity_tool(card_id=card_id, minutes_window=60)
        velocity_data = vel_res.get("data", {})
        velocity_count = velocity_data.get("transaction_count", 1)
        
        signals: List[Dict[str, Any]] = []
        
        # Velocity check
        if velocity_count >= 3:
            signals.append({
                "signal_id": "SIG_VELOCITY",
                "signal_type": "velocity_anomaly",
                "severity": "HIGH" if velocity_count >= 5 else "MEDIUM",
                "description": f"High transaction velocity: {velocity_count} txs in 60m",
                "score_impact": 20.0
            })
            
        # Amount anomaly check
        amount = tx.get("amount", 0.0)
        if amount > 5000.0:
            signals.append({
                "signal_id": "SIG_AMOUNT",
                "signal_type": "amount_anomaly",
                "severity": "HIGH",
                "description": f"High transaction amount ${amount:.2f}",
                "score_impact": 30.0
            })
            
        # Cross-border check
        if tx.get("is_international", False):
            signals.append({
                "signal_id": "SIG_INTL",
                "signal_type": "geographic_anomaly",
                "severity": "MEDIUM",
                "description": f"International transaction in {tx.get('merchant_country')}",
                "score_impact": 25.0
            })

        return {
            "agent_name": self.name,
            "status": "SUCCESS",
            "signals": signals,
            "velocity_count": velocity_count,
            "transaction": tx
        }

fraud_agent = FraudInvestigationAgent()
