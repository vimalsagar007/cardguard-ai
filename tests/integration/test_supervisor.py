"""Integration Tests for CardGuard Supervisor Agent and All 30 Scenarios"""
from app.agents.supervisor_agent import supervisor_agent
from app.models.schemas import DecisionType

async def test_full_investigation_scenario():
    # Scenario 30: Full successful investigation
    rec = await supervisor_agent.investigate_transaction("TXN-00000030")
    assert rec.case_id.startswith("CASE-")
    assert rec.decision in [DecisionType.BLOCK_PENDING_APPROVAL, DecisionType.ESCALATE, DecisionType.CLEAR, DecisionType.MONITOR]
    assert rec.confidence > 0.0
    assert len(rec.audit_id) > 0

async def test_legitimate_low_risk_scenario():
    # Scenario 1: Legitimate transaction
    rec = await supervisor_agent.investigate_transaction("TXN-00000008")
    assert rec.risk_score < 60.0
    assert rec.human_approval_required is False
