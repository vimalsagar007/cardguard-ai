"""Decision Specialist Agent"""
from typing import Dict, Any, List
from app.decision_engine.engine import decision_engine
from app.models.schemas import RiskAssessment, DecisionType, FraudSignal

class DecisionAgent:
    def __init__(self, name: str = "decision_agent"):
        self.name = name

    async def evaluate_decision(
        self,
        tx: Dict[str, Any],
        emp: Dict[str, Any],
        merch: Dict[str, Any],
        velocity_count: int,
        policy_violations: List[str]
    ) -> Dict[str, Any]:
        assessment, decision, human_req, signals = decision_engine.evaluate(
            tx=tx,
            emp=emp,
            merch=merch,
            velocity_count=velocity_count,
            policy_violations=policy_violations
        )

        return {
            "agent_name": self.name,
            "status": "SUCCESS",
            "assessment": assessment.model_dump(),
            "decision": decision.value,
            "human_approval_required": human_req,
            "signals": [s.model_dump() for s in signals]
        }

decision_agent = DecisionAgent()
