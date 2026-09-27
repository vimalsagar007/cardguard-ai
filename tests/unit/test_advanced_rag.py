"""Unit Tests for Advanced HyDE RAG Engine & Grounding Verification"""
import pytest
from app.rag.advanced_rag import advanced_rag_engine
from app.services.vertex_search_service import vertex_search_service

@pytest.mark.asyncio
async def test_expand_query():
    queries = await advanced_rag_engine.expand_query("international travel limit")
    assert len(queries) == 3
    assert "international travel limit" in queries[0]

@pytest.mark.asyncio
async def test_generate_hypothetical_document():
    hyde_doc = await advanced_rag_engine.generate_hypothetical_document("electronics limit")
    assert "electronics limit" in hyde_doc.lower() or "policy" in hyde_doc.lower()

@pytest.mark.asyncio
async def test_execute_advanced_rag():
    res = await advanced_rag_engine.execute_advanced_rag(
        query="international travel expense approval limit over 2500",
        top_k=3
    )
    assert res.original_query == "international travel expense approval limit over 2500"
    assert len(res.expanded_queries) == 3
    assert res.grounding_fidelity_score > 0.0
    assert len(res.citations) > 0
