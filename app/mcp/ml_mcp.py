"""XGBoost Machine Learning MCP Tool for CARDGUARD AI v2.0"""
import logging
from typing import Dict, Any, Optional
from app.mcp.base import mcp_tool, RiskClassification
from app.services.xgboost_service import xgboost_service

logger = logging.getLogger("cardguard.mcp.ml")

@mcp_tool(
    name="evaluate_xgboost_fraud_score_tool",
    description="Evaluates a structured corporate transaction using an XGBoost / Gradient Boosted Decision Trees (GBDT) model.",
    risk_classification=RiskClassification.READ_ONLY
)
async def evaluate_xgboost_fraud_score_tool(
    amount: float,
    single_tx_limit: float = 5000.0,
    velocity_count: int = 1,
    is_international: bool = False,
    is_high_risk_mcc: bool = False,
    is_approved_vendor: bool = True
) -> Dict[str, Any]:
    """MCP Tool executing XGBoost GBDT tree inference over transaction feature vectors."""
    try:
        tx = {"amount": amount, "is_international": is_international}
        emp = {"single_tx_limit": single_tx_limit}
        merch = {"is_high_risk_mcc": is_high_risk_mcc, "is_approved_vendor": is_approved_vendor}
        
        pred = xgboost_service.predict_fraud_probability(
            tx=tx,
            emp=emp,
            merch=merch,
            velocity_count=velocity_count
        )
        
        return {
            "status": "SUCCESS",
            "prediction": pred.model_dump()
        }
    except Exception as e:
        logger.error(f"XGBoost MCP Tool evaluation error: {e}")
        return {
            "status": "ERROR",
            "message": str(e)
        }
