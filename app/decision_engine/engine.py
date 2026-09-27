"""Deterministic Fraud Risk Engine"""
import logging
from typing import Dict, Any, List, Tuple
from app.models.schemas import RiskLevel, DecisionType, RiskAssessment, FraudSignal
from app.decision_engine.rules import ALL_RULES, RULE_AMOUNT_ANOMALY, RULE_HIGH_RISK_MCC, RULE_GEOGRAPHIC_JUMP, RULE_VELOCITY_ANOMALY, RULE_UNAPPROVED_VENDOR, RULE_HISTORICAL_FRAUD_MATCH

logger = logging.getLogger(__name__)

class DeterministicDecisionEngine:
    def __init__(self, rule_version: str = "v1.2.0"):
        self.rule_version = rule_version

    def evaluate(
        self,
        tx: Dict[str, Any],
        emp: Dict[str, Any],
        merch: Dict[str, Any],
        velocity_count: int,
        policy_violations: List[str]
    ) -> Tuple[RiskAssessment, DecisionType, bool, List[FraudSignal]]:
        """Evaluates deterministic risk rules and returns risk score, decision, human approval flag, and signals."""
        total_score = 0.0
        triggered_rule_ids = []
        signals: List[FraudSignal] = []

        amount = tx.get("amount", 0.0)
        single_limit = emp.get("single_tx_limit", 5000.0) if emp else 5000.0
        
        # Rule 1: Amount Anomaly
        if amount > single_limit:
            score_impact = min(30.0, RULE_AMOUNT_ANOMALY.weight * (amount / single_limit))
            total_score += score_impact
            triggered_rule_ids.append(RULE_AMOUNT_ANOMALY.rule_id)
            signals.append(FraudSignal(
                signal_id="SIG_AMOUNT_EXCEEDED",
                signal_type="amount_anomaly",
                severity=RiskLevel.HIGH if amount > single_limit * 2 else RiskLevel.MEDIUM,
                description=f"Transaction amount ${amount:.2f} exceeds employee single limit ${single_limit:.2f}",
                score_impact=score_impact,
                raw_metrics={"amount": amount, "single_limit": single_limit}
            ))

        # Rule 2: High Risk MCC
        is_high_mcc = merch.get("is_high_risk_mcc", False) if merch else False
        if is_high_mcc:
            total_score += RULE_HIGH_RISK_MCC.weight
            triggered_rule_ids.append(RULE_HIGH_RISK_MCC.rule_id)
            signals.append(FraudSignal(
                signal_id="SIG_HIGH_RISK_MCC",
                signal_type="merchant_risk",
                severity=RiskLevel.HIGH,
                description=f"Merchant {merch.get('merchant_name')} operates under restricted MCC category ({merch.get('merchant_category_code')})",
                score_impact=RULE_HIGH_RISK_MCC.weight,
                raw_metrics={"mcc": merch.get("merchant_category_code")}
            ))

        # Rule 3: Geographic Jump / International Anomaly
        if tx.get("is_international", False):
            total_score += RULE_GEOGRAPHIC_JUMP.weight
            triggered_rule_ids.append(RULE_GEOGRAPHIC_JUMP.rule_id)
            signals.append(FraudSignal(
                signal_id="SIG_INTL_GEO_JUMP",
                signal_type="geographic_anomaly",
                severity=RiskLevel.MEDIUM,
                description=f"Cross-border transaction in {tx.get('merchant_country')} without registered travel notification",
                score_impact=RULE_GEOGRAPHIC_JUMP.weight,
                raw_metrics={"country": tx.get("merchant_country")}
            ))

        # Rule 4: Velocity Anomaly
        if velocity_count >= 3:
            total_score += RULE_VELOCITY_ANOMALY.weight
            triggered_rule_ids.append(RULE_VELOCITY_ANOMALY.rule_id)
            signals.append(FraudSignal(
                signal_id="SIG_CARD_VELOCITY_SPIKE",
                signal_type="velocity_anomaly",
                severity=RiskLevel.MEDIUM,
                description=f"Card velocity spike detected ({velocity_count} transactions in short window)",
                score_impact=RULE_VELOCITY_ANOMALY.weight,
                raw_metrics={"velocity_count": velocity_count}
            ))

        # Rule 5: Unapproved Vendor
        if merch and not merch.get("is_approved_vendor", True):
            total_score += RULE_UNAPPROVED_VENDOR.weight
            triggered_rule_ids.append(RULE_UNAPPROVED_VENDOR.rule_id)
            signals.append(FraudSignal(
                signal_id="SIG_UNAPPROVED_VENDOR",
                signal_type="merchant_risk",
                severity=RiskLevel.LOW,
                description=f"Merchant {merch.get('merchant_name')} is not listed in corporate preferred vendor directory",
                score_impact=RULE_UNAPPROVED_VENDOR.weight,
                raw_metrics={"is_approved_vendor": False}
            ))

        # Cap score at 100
        final_score = min(100.0, round(total_score, 1))

        # Determine Risk Level Tier
        if final_score < 30.0:
            risk_level = RiskLevel.LOW
            decision = DecisionType.CLEAR
            human_approval_required = False
        elif final_score < 60.0:
            risk_level = RiskLevel.MEDIUM
            decision = DecisionType.MONITOR
            human_approval_required = False
        elif final_score < 85.0:
            risk_level = RiskLevel.HIGH
            decision = DecisionType.ESCALATE
            human_approval_required = True
        else:
            risk_level = RiskLevel.CRITICAL
            decision = DecisionType.BLOCK_PENDING_APPROVAL
            human_approval_required = True

        assessment = RiskAssessment(
            rule_version=self.rule_version,
            total_risk_score=final_score,
            risk_level=risk_level,
            triggered_rules=triggered_rule_ids,
            input_metrics={
                "amount": amount,
                "single_limit": single_limit,
                "velocity_count": velocity_count,
                "is_international": tx.get("is_international", False)
            }
        )

        return assessment, decision, human_approval_required, signals

decision_engine = DeterministicDecisionEngine()
