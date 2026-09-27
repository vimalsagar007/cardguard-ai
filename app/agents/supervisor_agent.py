"""CardGuard Supervisor Agent (ADK Orchestrator)"""
import asyncio
import uuid
import logging
from datetime import datetime
from typing import Dict, Any, List
from app.agents.fraud_agent import fraud_agent
from app.agents.policy_agent import policy_agent
from app.agents.merchant_agent import merchant_agent
from app.agents.employee_agent import employee_agent
from app.agents.case_agent import case_agent
from app.agents.decision_agent import decision_agent
from app.mcp.transaction_mcp import get_transaction_tool
from app.models.schemas import DecisionRecommendation, RiskLevel, DecisionType, Citation, Evidence, FraudSignal

logger = logging.getLogger(__name__)

class CardGuardSupervisorAgent:
    def __init__(self, name: str = "supervisor_agent"):
        self.name = name

    async def investigate_transaction(self, transaction_id: str, correlation_id: str = None) -> DecisionRecommendation:
        correlation_id = correlation_id or f"CORR-{uuid.uuid4().hex[:8]}"
        audit_id = f"AUDIT-{uuid.uuid4().hex[:8]}"
        logger.info(f"[{self.name}] Starting parallel fraud investigation for tx: {transaction_id} (Correlation: {correlation_id})")

        # Step 1: Fetch initial transaction details
        tx_res = await get_transaction_tool(transaction_id=transaction_id)
        tx = tx_res.get("data", {})
        if "error" in tx or not tx:
            raise ValueError(f"Transaction {transaction_id} not found.")

        card_id = tx.get("card_id", "UNKNOWN_CARD")
        employee_id = tx.get("employee_id", "UNKNOWN_EMP")
        merchant_id = tx.get("merchant_id", "UNKNOWN_MERCH")
        amount = tx.get("amount", 0.0)

        # Step 2: Parallel Delegation to Specialist Agents
        logger.info(f"[{self.name}] Executing parallel fan-out to Fraud, Policy, Merchant, Employee agents...")
        fraud_task = fraud_agent.investigate(transaction_id=transaction_id, card_id=card_id)
        policy_task = policy_agent.investigate(transaction_amount=amount, merchant_category=tx.get("merchant_category_code", ""))
        merchant_task = merchant_agent.investigate(merchant_id=merchant_id)
        employee_task = employee_agent.investigate(employee_id=employee_id, current_amount=amount)

        fraud_res, policy_res, merchant_res, employee_res = await asyncio.gather(
            fraud_task, policy_task, merchant_task, employee_task
        )

        # Step 3: Aggregate findings & signals
        fraud_signals_raw = fraud_res.get("signals", [])
        fraud_signals = [FraudSignal(**s) for s in fraud_signals_raw]

        policy_finding_raw = policy_res.get("policy_finding", {})
        policy_violations = [policy_finding_raw["violation_details"]] if policy_finding_raw.get("violation_details") else []

        citations_raw = policy_res.get("citations", [])
        citations = [Citation(**c) for c in citations_raw]

        merchant_finding_raw = merchant_res.get("merchant_finding", {})
        employee_finding_raw = employee_res.get("employee_finding", {})

        # Step 4: Deterministic Decision Engine Evaluation
        decision_res = await decision_agent.evaluate_decision(
            tx=tx,
            emp=employee_res.get("raw_employee", {}),
            merch=merchant_res.get("raw_merchant", {}),
            velocity_count=fraud_res.get("velocity_count", 1),
            policy_violations=policy_violations
        )

        assessment = decision_res.get("assessment", {})
        risk_score = assessment.get("total_risk_score", 0.0)
        risk_level = RiskLevel(assessment.get("risk_level", "LOW"))
        decision_type = DecisionType(decision_res.get("decision", "CLEAR"))
        human_req = decision_res.get("human_approval_required", False)

        # Merge decision signals
        for s in decision_res.get("signals", []):
            if not any(fs.signal_id == s["signal_id"] for fs in fraud_signals):
                fraud_signals.append(FraudSignal(**s))

        # Step 5: Create / Update Case via Case Agent
        case_res = await case_agent.create_or_update_case(
            transaction_id=transaction_id,
            risk_level=risk_level,
            risk_score=risk_score,
            decision=decision_type,
            summary=f"Automated investigation finished for tx {transaction_id}"
        )
        case_id = case_res.get("case_id", f"CASE-{transaction_id}")

        # Step 6: Assemble Grounded Decision Recommendation
        evidence_list = [
            Evidence(
                evidence_id=f"EVID-{uuid.uuid4().hex[:6]}",
                source_type="transaction_log",
                title="Transaction Velocity Log",
                summary=f"Observed {fraud_res.get('velocity_count')} transactions in 60m window for card {card_id}",
                source_ref=f"bq://cardguard_fraud_db.transactions/{transaction_id}"
            ),
            Evidence(
                evidence_id=f"EVID-{uuid.uuid4().hex[:6]}",
                source_type="merchant_db",
                title="Merchant Risk Classification",
                summary=f"Merchant {merchant_finding_raw.get('merchant_name')} risk score: {merchant_finding_raw.get('risk_score')}",
                source_ref=f"bq://cardguard_fraud_db.merchants/{merchant_id}"
            )
        ]

        rec = DecisionRecommendation(
            case_id=case_id,
            transaction_id=transaction_id,
            risk_level=risk_level,
            risk_score=risk_score,
            decision=decision_type,
            reason_codes=assessment.get("triggered_rules", []),
            fraud_signals=fraud_signals,
            policy_findings=[policy_finding_raw] if policy_finding_raw else [],
            merchant_findings=[merchant_finding_raw] if merchant_finding_raw else [],
            employee_findings=[employee_finding_raw] if employee_finding_raw else [],
            evidence=evidence_list,
            citations=citations,
            missing_evidence=[],
            confidence=0.95,
            human_approval_required=human_req,
            recommended_actions=[
                "Review geographic velocity logs",
                "Request pre-approval documentation from employee"
            ] if human_req else ["Auto-close investigation"],
            audit_id=audit_id
        )

        logger.info(f"[{self.name}] Investigation finished for {transaction_id}: Risk Score={risk_score:.1f}, Decision={decision_type.value}")
        return rec

supervisor_agent = CardGuardSupervisorAgent()
