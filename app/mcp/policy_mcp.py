"""Policy MCP Tools"""
from typing import Dict, Any, List
from app.mcp.base import mcp_tool, RiskClassification
from app.rag.retriever import rag_retriever
from app.rag.grounding import grounding_verifier, UNAVAILABLE_CLAIM_TEXT

@mcp_tool(
    name="retrieve_policy_clauses",
    description="Query corporate policy RAG vector store for relevant policy clauses and citations",
    risk_classification=RiskClassification.READ_ONLY
)
async def retrieve_policy_clauses_tool(query: str, top_k: int = 3, **kwargs) -> Dict[str, Any]:
    retrieved = await rag_retriever.retrieve(query, top_k=top_k)
    if not retrieved:
        return {
            "query": query,
            "citations": [],
            "grounding_status": "UNGROUNDED",
            "message": UNAVAILABLE_CLAIM_TEXT
        }
        
    citations = []
    for chunk, score in retrieved:
        citations.append({
            "citation_id": chunk.chunk_id,
            "document_name": chunk.document_name,
            "section_title": chunk.section_title,
            "clause_text": chunk.text,
            "relevance_score": score
        })
        
    return {
        "query": query,
        "citations": citations,
        "grounding_status": "GROUNDED"
    }
