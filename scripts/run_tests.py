"""CardGuard AI Test Suite Runner"""
import sys
import os
import asyncio

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tests.unit.test_rules import test_legitimate_transaction, test_high_value_policy_violation
from tests.security.test_prompt_injection import test_prompt_injection_sanitization, test_unauthorized_high_risk_tool_execution_blocked
from tests.integration.test_supervisor import test_full_investigation_scenario, test_legitimate_low_risk_scenario

async def main():
    print("==================================================")
    print("RUNNING CARDGUARD AI UNIT, SECURITY & INTEGRATION TESTS")
    print("==================================================")

    print("\n[1/3] Running Decision Engine Unit Tests...")
    test_legitimate_transaction()
    test_high_value_policy_violation()
    print("  ✓ Unit tests passed!")

    print("\n[2/3] Running Prompt Injection & Security Tests...")
    test_prompt_injection_sanitization()
    await test_unauthorized_high_risk_tool_execution_blocked()
    print("  ✓ Security tests passed!")

    print("\n[3/3] Running Supervisor Multi-Agent Integration Tests...")
    await test_full_investigation_scenario()
    await test_legitimate_low_risk_scenario()
    print("  ✓ Integration tests passed!")

    print("\n==================================================")
    print("ALL TEST SUITES PASSED SUCCESSFULLY!")
    print("==================================================")

if __name__ == "__main__":
    asyncio.run(main())
