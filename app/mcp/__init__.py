from app.mcp.employee_mcp import get_employee_profile_tool
from app.mcp.merchant_mcp import get_merchant_risk_profile_tool
from app.mcp.policy_mcp import retrieve_policy_clauses_tool
from app.mcp.case_mcp import update_case_status_tool
from app.mcp.decision_mcp import execute_card_block_action_tool
from app.mcp.document_mcp import process_expense_receipt_tool
from app.mcp.vertex_rag_mcp import search_vertex_policy_datastore_tool, advanced_rag_policy_query_tool

ALL_MCP_TOOLS = [
    get_employee_profile_tool,
    get_merchant_risk_profile_tool,
    retrieve_policy_clauses_tool,
    update_case_status_tool,
    execute_card_block_action_tool,
    process_expense_receipt_tool,
    search_vertex_policy_datastore_tool,
    advanced_rag_policy_query_tool
]

__all__ = [
    "get_employee_profile_tool",
    "get_merchant_risk_profile_tool",
    "retrieve_policy_clauses_tool",
    "update_case_status_tool",
    "execute_card_block_action_tool",
    "process_expense_receipt_tool",
    "search_vertex_policy_datastore_tool",
    "advanced_rag_policy_query_tool",
    "ALL_MCP_TOOLS"
]
