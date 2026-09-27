from app.mcp.employee_mcp import get_employee_profile_tool
from app.mcp.merchant_mcp import check_merchant_risk_mcc_tool
from app.mcp.policy_mcp import search_policy_knowledge_vector_tool
from app.mcp.case_mcp import update_case_status_tool
from app.mcp.decision_mcp import execute_card_block_action_tool
from app.mcp.document_mcp import process_expense_receipt_tool
from app.mcp.vertex_rag_mcp import search_vertex_policy_datastore_tool, advanced_rag_policy_query_tool

ALL_MCP_TOOLS = [
    get_employee_profile_tool,
    check_merchant_risk_mcc_tool,
    search_policy_knowledge_vector_tool,
    update_case_status_tool,
    execute_card_block_action_tool,
    process_expense_receipt_tool,
    search_vertex_policy_datastore_tool,
    advanced_rag_policy_query_tool
]

__all__ = [
    "get_employee_profile_tool",
    "check_merchant_risk_mcc_tool",
    "search_policy_knowledge_vector_tool",
    "update_case_status_tool",
    "execute_card_block_action_tool",
    "process_expense_receipt_tool",
    "search_vertex_policy_datastore_tool",
    "advanced_rag_policy_query_tool",
    "ALL_MCP_TOOLS"
]
