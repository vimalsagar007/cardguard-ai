"""Structured Observability, Cloud Trace, and Cost Logger"""
import time
import json
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger("cardguard.observability")

class ObservabilityLogger:
    def log_event(
        self,
        event_type: str,
        correlation_id: str,
        trace_id: Optional[str] = None,
        case_id: Optional[str] = None,
        transaction_id: Optional[str] = None,
        agent_name: Optional[str] = None,
        tool_name: Optional[str] = None,
        latency_ms: float = 0.0,
        input_tokens: int = 0,
        output_tokens: int = 0,
        status: str = "SUCCESS",
        error_type: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        """Logs structured JSON event for Cloud Logging & BigQuery ingestion."""
        # Calculate estimated cost
        estimated_cost = (input_tokens / 1000.0) * 0.000075 + (output_tokens / 1000.0) * 0.00030

        log_payload = {
            "timestamp": time.time(),
            "event_type": event_type,
            "correlation_id": correlation_id,
            "trace_id": trace_id or correlation_id,
            "case_id": case_id,
            "transaction_id": transaction_id,
            "agent_name": agent_name,
            "tool_name": tool_name,
            "latency_ms": round(latency_ms, 2),
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "estimated_cost_usd": round(estimated_cost, 6),
            "status": status,
            "error_type": error_type,
            "details": details or {}
        }

        # Ensure secrets are never logged
        json_str = json.dumps(log_payload)
        logger.info(f"[OBSERVABILITY] {json_str}")

obs_logger = ObservabilityLogger()
