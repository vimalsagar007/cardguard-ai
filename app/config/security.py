"""Security Guardrails and Prompt Injection Defense Engine"""
import re
import logging
from typing import Tuple, List

logger = logging.getLogger(__name__)

PROMPT_INJECTION_PATTERNS = [
    r"ignore\s+(previous|all)\s+instructions",
    r"approve\s+this\s+transaction",
    r"reveal\s+system\s+prompt",
    r"call\s+delete_case",
    r"ignore\s+the\s+policy",
    r"override\s+security",
    r"act\s+as\s+admin",
    r"sudo\s+",
    r"bypass\s+risk\s+check"
]

class PromptInjectionDefense:
    def sanitize_input(self, user_input: str) -> Tuple[str, bool]:
        """Scans user input or retrieved context for prompt injection patterns."""
        if not user_input:
            return "", False

        cleaned = user_input
        injection_detected = False

        for pattern in PROMPT_INJECTION_PATTERNS:
            if re.search(pattern, cleaned, re.IGNORECASE):
                logger.warning(f"[SECURITY ALERT] Detected prompt injection attempt matching pattern: '{pattern}'")
                injection_detected = True
                cleaned = re.sub(pattern, "[BLOCKED_INJECTION_ATTEMPT]", cleaned, flags=re.IGNORECASE)

        return cleaned, injection_detected

    def validate_tool_execution(self, tool_name: str, risk_classification: str, is_human_authorized: bool) -> bool:
        """Validates tool execution boundaries."""
        if risk_classification == "HIGH_RISK_WRITE" and not is_human_authorized:
            logger.error(f"[SECURITY BLOCKED] Unauthorized attempt to invoke HIGH_RISK_WRITE tool '{tool_name}' without human approval.")
            return False
        return True

security_defense = PromptInjectionDefense()
