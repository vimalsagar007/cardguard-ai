"""Deterministic Fraud Risk Rules Definition"""
from typing import Dict, Any, List, Tuple
from app.models.schemas import RiskLevel, DecisionType, FraudSignal

class RiskRule:
    def __init__(self, rule_id: str, name: str, description: str, weight: float, threshold: float):
        self.rule_id = rule_id
        self.name = name
        self.description = description
        self.weight = weight
        self.threshold = threshold

# Standard Rule Registry (Version 1.2.0)
RULE_AMOUNT_ANOMALY = RiskRule("R001", "Amount Exceeds Employee Single Limit", "Transaction amount exceeds employee assigned single transaction limit", weight=30.0, threshold=1.0)
RULE_HIGH_RISK_MCC = RiskRule("R002", "Restricted High Risk Merchant Category", "Transaction conducted at high-risk MCC (Gambling, Crypto, Jewelry)", weight=40.0, threshold=1.0)
RULE_GEOGRAPHIC_JUMP = RiskRule("R003", "Geographic Impossible Velocity Jump", "Transaction conducted internationally without prior travel request", weight=25.0, threshold=1.0)
RULE_VELOCITY_ANOMALY = RiskRule("R004", "Card Rapid Velocity Spike", "Card velocity exceeds 5 transactions per hour", weight=20.0, threshold=5.0)
RULE_UNAPPROVED_VENDOR = RiskRule("R005", "Unapproved Vendor Category", "Merchant is not in approved corporate vendor directory", weight=10.0, threshold=1.0)
RULE_HISTORICAL_FRAUD_MATCH = RiskRule("R006", "Historical Fraud Pattern Match", "Transaction matches known historical split-transaction or stolen card pattern", weight=35.0, threshold=1.0)

ALL_RULES = [
    RULE_AMOUNT_ANOMALY,
    RULE_HIGH_RISK_MCC,
    RULE_GEOGRAPHIC_JUMP,
    RULE_VELOCITY_ANOMALY,
    RULE_UNAPPROVED_VENDOR,
    RULE_HISTORICAL_FRAUD_MATCH
]
