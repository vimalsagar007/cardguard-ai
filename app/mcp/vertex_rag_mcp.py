"""Vertex AI Search & Advanced RAG MCP Tools for CARDGUARD AI v2.0"""
import json
from typing import Dict, Any, Optional

from app.mcp.base import mcp_tool, RiskClassification
from app.services.vertex_search_service import vertex_search_service
from app.rag.advanced_rag import advanced_rag_engine

@mcp_tool(
    name="search_vertex_policy_datastore_tool",
    description="Performs hybrid dense vector + sparse keyword search over Google Cloud Vertex AI Search Datastore for corporate fraud policies.",
    risk_classification=RiskClassification.READ_ONLY
)
async def search_vertex_policy_datastore_tool(
    query: str,
    top_k: int = 4
) -> str:
    """MCP tool for searching Vertex AI Search Datastore."""
    res = await vertex_search_service.search_datastore(query=query, page_size=top_k)
    return json.dumps(res.model_dump(), indent=2)

@mcp_tool(
    name="advanced_rag_policy_query_tool",
    description="Executes HyDE hypothetical document expansion, multi-query expansion, contextual compression, and grounding fidelity scoring on Vertex AI Search policy datastores.",
    risk_classification=RiskClassification.READ_ONLY
)
async def advanced_rag_policy_query_tool(
    query: str,
    top_k: int = 4
) -> str:
    """MCP tool for Advanced HyDE RAG policy query."""
    res = await advanced_rag_engine.execute_advanced_rag(query=query, top_k=top_k)
    return json.dumps(res.model_dump(), indent=2)
