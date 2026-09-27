"""Unit Tests for Deterministic Decision Engine Rules"""
from app.decision_engine.engine import decision_engine
from app.models.schemas import RiskLevel, DecisionType

def test_legitimate_transaction():
    tx = {"amount": 100.0, "is_international": False}
    emp = {"single_tx_limit": 5000.0}
    merch = {"is_high_risk_mcc": False, "is_approved_vendor": True}
    
    assessment, decision, human_req, signals = decision_engine.evaluate(tx, emp, merch, velocity_count=1, policy_violations=[])
    assert decision == DecisionType.CLEAR
    assert assessment.total_risk_score < 30.0
    assert human_req is False

def test_high_value_policy_violation():
    tx = {"amount": 15000.0, "is_international": True}
    emp = {"single_tx_limit": 5000.0}
    merch = {"is_high_risk_mcc": True, "merchant_category_code": "6051", "is_approved_vendor": False}
    
    assessment, decision, human_req, signals = decision_engine.evaluate(tx, emp, merch, velocity_count=4, policy_violations=["Amount exceeds limit"])
    assert decision == DecisionType.BLOCK_PENDING_APPROVAL
    assert assessment.total_risk_score >= 85.0
    assert human_req is True
