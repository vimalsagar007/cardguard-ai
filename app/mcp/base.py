"""Base Model Context Protocol (MCP) Tool Abstraction with Circuit Breakers & Risk Enforcement"""
import asyncio
import logging
import functools
from datetime import datetime
from typing import Callable, Any, Dict, Optional
from pydantic import BaseModel
from app.models.schemas import RiskClassification

logger = logging.getLogger(__name__)

class MCPToolMetadata(BaseModel):
    name: str
    description: str
    tool_version: str = "1.0.0"
    tool_owner: str = "Platform Security & Risk Team"
    risk_classification: RiskClassification
    timeout_seconds: float = 10.0
    max_retries: int = 3
    is_idempotent: bool = True

class MCPException(Exception):
    """Structured MCP Tool Error"""
    def __init__(self, tool_name: str, message: str, error_code: str = "MCP_ERROR"):
        self.tool_name = tool_name
        self.message = message
        self.error_code = error_code
        super().__init__(f"[{tool_name}] {error_code}: {message}")

def mcp_tool(
    name: str,
    description: str,
    risk_classification: RiskClassification,
    tool_version: str = "1.0.0",
    timeout_seconds: float = 10.0,
    max_retries: int = 3,
    is_idempotent: bool = True
):
    """Decorator to enforce MCP tool safety, risk limits, retries, timeouts, and audit logging."""
    metadata = MCPToolMetadata(
        name=name,
        description=description,
        tool_version=tool_version,
        risk_classification=risk_classification,
        timeout_seconds=timeout_seconds,
        max_retries=max_retries,
        is_idempotent=is_idempotent
    )

    def decorator(func: Callable):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> Dict[str, Any]:
            # 1. Enforce HIGH_RISK_WRITE restriction
            if metadata.risk_classification == RiskClassification.HIGH_RISK_WRITE:
                if not kwargs.get("human_authorized", False):
                    raise MCPException(
                        tool_name=name,
                        message="HIGH_RISK_WRITE tools require explicit human approval authorization.",
                        error_code="UNAUTHORIZED_HIGH_RISK_EXECUTION"
                    )

            # 2. Audit Logging Before Call
            start_time = datetime.utcnow()
            logger.info(f"[MCP AUDIT] Invoking tool '{name}' (Risk: {metadata.risk_classification.value}) args={kwargs}")

            # 3. Execution with Timeout & Exponential Retry
            attempts = 0
            last_err = None
            while attempts < (metadata.max_retries if metadata.is_idempotent else 1):
                attempts += 1
                try:
                    res = await asyncio.wait_for(func(*args, **kwargs), timeout=metadata.timeout_seconds)
                    elapsed = (datetime.utcnow() - start_time).total_seconds() * 1000
                    logger.info(f"[MCP AUDIT] Tool '{name}' succeeded in {elapsed:.1f}ms")
                    return {
                        "status": "SUCCESS",
                        "tool_name": name,
                        "risk_classification": metadata.risk_classification.value,
                        "data": res
                    }
                except asyncio.TimeoutError:
                    last_err = MCPException(name, f"Execution timed out after {metadata.timeout_seconds}s", "TIMEOUT")
                    logger.warning(f"[MCP RETRY] Tool '{name}' attempt {attempts} timed out.")
                except Exception as e:
                    last_err = e
                    logger.warning(f"[MCP RETRY] Tool '{name}' attempt {attempts} failed: {e}")
                
                if attempts < metadata.max_retries and metadata.is_idempotent:
                    await asyncio.sleep(0.2 * (2 ** (attempts - 1)))

            raise MCPException(name, f"Tool failed after {attempts} attempts. Last error: {last_err}", "EXECUTION_FAILED")

        wrapper.metadata = metadata
        return wrapper
    return decorator
