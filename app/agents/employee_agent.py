"""Employee Specialist Agent"""
from typing import Dict, Any
from app.mcp.employee_mcp import get_employee_profile_tool
from app.models.schemas import EmployeeFinding

class EmployeeAgent:
    def __init__(self, name: str = "employee_agent"):
        self.name = name

    async def investigate(self, employee_id: str, current_amount: float) -> Dict[str, Any]:
        res = await get_employee_profile_tool(employee_id=employee_id)
        emp = res.get("data", {})
        
        limit = emp.get("single_tx_limit", 5000.0)
        avg = emp.get("historical_avg_tx_amount", 150.0)
        deviation = ((current_amount - avg) / avg * 100.0) if avg > 0 else 0.0
        
        finding = EmployeeFinding(
            employee_id=employee_id,
            department=emp.get("department", "General"),
            single_tx_limit=limit,
            monthly_spending_limit=emp.get("monthly_spending_limit", 20000.0),
            historical_avg_tx_amount=avg,
            historical_fraud_cases_count=emp.get("historical_fraud_cases_count", 0),
            deviation_from_baseline=round(min(999.0, max(0.0, deviation)), 1)
        )

        return {
            "agent_name": self.name,
            "status": "SUCCESS",
            "employee_finding": finding.model_dump(),
            "raw_employee": emp
        }

employee_agent = EmployeeAgent()
