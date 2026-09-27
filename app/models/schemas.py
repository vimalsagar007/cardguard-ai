"""Pydantic Data Models for CardGuard AI"""
from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict

class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class DecisionType(str, Enum):
    CLEAR = "CLEAR"
    MONITOR = "MONITOR"
    ESCALATE = "ESCALATE"
    BLOCK_PENDING_APPROVAL = "BLOCK_PENDING_APPROVAL"

class RiskClassification(str, Enum):
    READ_ONLY = "READ_ONLY"
    LOW_RISK_WRITE = "LOW_RISK_WRITE"
    HIGH_RISK_WRITE = "HIGH_RISK_WRITE"

class Transaction(BaseModel):
    transaction_id: str = Field(description="Unique transaction ID")
    card_id: str = Field(description="Synthetic masked card ID (e.g. CARD-9876)")
    employee_id: str = Field(description="Employee ID")
    merchant_id: str = Field(description="Merchant ID")
    merchant_name: str = Field(description="Merchant Name")
    merchant_category_code: str = Field(description="MCC code")
    merchant_country: str = Field(default="US", description="Merchant ISO Country Code")
    amount: float = Field(description="Transaction amount in USD")
    currency: str = Field(default="USD", description="Currency code")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Transaction timestamp")
    location_city: str = Field(default="New York", description="Transaction city")
    location_country: str = Field(default="US", description="Transaction country")
    pos_entry_mode: str = Field(default="CHIP", description="POS entry mode")
    is_international: bool = Field(default=False, description="Is international transaction")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional transaction attributes")

class FraudSignal(BaseModel):
    signal_id: str = Field(description="Signal identifier")
    signal_type: str = Field(description="Type of signal (velocity, geo_jump, amount_anomaly, merchant_risk)")
    severity: RiskLevel = Field(description="Signal severity level")
    description: str = Field(description="Human readable explanation")
    score_impact: float = Field(description="Impact on total risk score (0 to 100)")
    raw_metrics: Dict[str, Any] = Field(default_factory=dict, description="Metric values triggering signal")

class Evidence(BaseModel):
    evidence_id: str = Field(description="Evidence ID")
    source_type: str = Field(description="Source type (transaction_log, policy_doc, merchant_db, employee_history)")
    title: str = Field(description="Brief evidence title")
    summary: str = Field(description="Detailed summary of evidence")
    source_ref: str = Field(description="File URI, URL, or BQ table reference")
    confidence: float = Field(default=1.0, ge=0.0, le=1.0, description="Evidence confidence score")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class Citation(BaseModel):
    citation_id: str = Field(description="Citation ID")
    document_name: str = Field(description="Policy document name (e.g. travel_policy.pdf)")
    section_title: Optional[str] = Field(default=None, description="Section or clause header")
    clause_text: str = Field(description="Exact retrieved clause text")
    effective_date: str = Field(default="2026-01-01", description="Policy effective date")
    version: str = Field(default="v1.0", description="Policy version")
    relevance_score: float = Field(default=1.0, ge=0.0, le=1.0)

class PolicyFinding(BaseModel):
    policy_id: str = Field(description="Policy identifier")
    policy_name: str = Field(description="Name of the corporate policy")
    clause_id: str = Field(description="Clause ID or title")
    is_compliant: bool = Field(description="Whether the transaction complies with policy")
    violation_details: Optional[str] = Field(default=None, description="Details if non-compliant")
    citations: List[Citation] = Field(default_factory=list, description="Supporting citations")

class MerchantFinding(BaseModel):
    merchant_id: str = Field(description="Merchant ID")
    merchant_name: str = Field(description="Merchant Name")
    risk_score: float = Field(description="Historical merchant risk score (0-100)")
    historical_chargeback_rate: float = Field(description="Chargeback rate %")
    is_high_risk_mcc: bool = Field(description="High risk MCC flag")
    is_approved_vendor: bool = Field(description="In approved vendor directory")
    notes: str = Field(description="Analysis summary")

class EmployeeFinding(BaseModel):
    employee_id: str = Field(description="Employee ID")
    department: str = Field(description="Employee department")
    single_tx_limit: float = Field(description="Employee card single tx limit")
    monthly_spending_limit: float = Field(description="Monthly spending limit")
    historical_avg_tx_amount: float = Field(description="Historical average tx amount")
    historical_fraud_cases_count: int = Field(default=0, description="Previous fraud cases count")
    deviation_from_baseline: float = Field(description="Percentage deviation from baseline (0-100%)")

class InvestigationPlan(BaseModel):
    case_id: str = Field(description="Associated case ID")
    tasks: List[Dict[str, Any]] = Field(description="List of planned investigation sub-tasks")
    parallel_groups: List[List[str]] = Field(description="Task groups that can execute in parallel")
    required_agents: List[str] = Field(description="Sub-agents involved")

class AgentFinding(BaseModel):
    agent_name: str = Field(description="Name of agent producing finding")
    task_id: str = Field(description="Task ID")
    status: str = Field(default="SUCCESS", description="Execution status")
    summary: str = Field(description="Key finding summary")
    evidence: List[Evidence] = Field(default_factory=list)
    signals: List[FraudSignal] = Field(default_factory=list)

class RiskAssessment(BaseModel):
    rule_version: str = Field(default="v1.2.0", description="Rule engine version")
    total_risk_score: float = Field(ge=0.0, le=100.0, description="Calculated risk score 0-100")
    risk_level: RiskLevel = Field(description="Risk level tier")
    triggered_rules: List[str] = Field(default_factory=list, description="Rule IDs triggered")
    input_metrics: Dict[str, Any] = Field(default_factory=dict, description="Rule input values")
    calculated_at: datetime = Field(default_factory=datetime.utcnow)

class DecisionRecommendation(BaseModel):
    case_id: str = Field(description="Case ID")
    transaction_id: str = Field(description="Transaction ID")
    risk_level: RiskLevel = Field(description="Overall risk level")
    risk_score: float = Field(description="Computed risk score")
    decision: DecisionType = Field(description="Recommended decision action")
    reason_codes: List[str] = Field(default_factory=list, description="Reason codes for decision")
    fraud_signals: List[FraudSignal] = Field(default_factory=list)
    policy_findings: List[PolicyFinding] = Field(default_factory=list)
    merchant_findings: List[MerchantFinding] = Field(default_factory=list)
    employee_findings: List[EmployeeFinding] = Field(default_factory=list)
    evidence: List[Evidence] = Field(default_factory=list)
    citations: List[Citation] = Field(default_factory=list)
    missing_evidence: List[str] = Field(default_factory=list, description="Missing required evidence")
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence score")
    human_approval_required: bool = Field(description="Whether human approval is required")
    recommended_actions: List[str] = Field(default_factory=list, description="Suggested next steps")
    audit_id: str = Field(description="Unique audit trail record ID")

class HumanApproval(BaseModel):
    case_id: str = Field(description="Case ID")
    approver_id: str = Field(description="Analyst ID")
    action: str = Field(description="APPROVED | REJECTED")
    comments: str = Field(description="Analyst reasoning comments")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class Case(BaseModel):
    case_id: str = Field(description="Unique Case ID")
    transaction_id: str = Field(description="Associated Transaction ID")
    status: str = Field(default="OPEN", description="OPEN | IN_INVESTIGATION | PENDING_APPROVAL | CLOSED")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    assigned_reviewer: Optional[str] = Field(default=None)
    risk_level: RiskLevel = Field(default=RiskLevel.MEDIUM)
    risk_score: float = Field(default=0.0)
    investigation_summary: Optional[str] = Field(default=None)
    decision: Optional[DecisionType] = Field(default=None)
    human_approval: Optional[HumanApproval] = Field(default=None)
    timeline: List[Dict[str, Any]] = Field(default_factory=list, description="Chronological timeline events")

class AuditEvent(BaseModel):
    audit_id: str = Field(description="Audit event ID")
    correlation_id: str = Field(description="Correlation ID for trace")
    trace_id: Optional[str] = Field(default=None)
    case_id: str = Field(description="Associated case ID")
    transaction_id: str = Field(description="Transaction ID")
    agent_name: str = Field(description="Agent or system component")
    action_type: str = Field(description="Action executed (TOOL_CALL | AGENT_DELEGATION | DECISION | HITL_APPROVAL)")
    details: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class InvestigationRequest(BaseModel):
    transaction_id: str = Field(description="Transaction ID to investigate")
    force_reinvestigation: bool = Field(default=False, description="Re-run investigation if case exists")
    requested_by: str = Field(default="SYSTEM", description="Originator of request")
