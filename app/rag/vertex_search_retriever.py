"""Vertex AI Search Hybrid Retriever Adapter for CARDGUARD AI v2.0"""
import logging
from typing import List, Dict, Any, Optional

from app.services.vertex_search_service import vertex_search_service, VertexSearchDocument

logger = logging.getLogger("cardguard.rag.vertex_retriever")

class VertexSearchRetriever:
    """Adapter for hybrid dense vector + sparse keyword retrieval via Vertex AI Search."""

    def __init__(self, datastore_id: str = "cardguard-policy-datastore"):
        self.datastore_id = datastore_id

    async def get_relevant_documents(
        self,
        query: str,
        top_k: int = 4,
        category_filter: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Retrieve relevant grounded policy documents matching the query."""
        filter_expr = f'category = "{category_filter}"' if category_filter else None
        res = await vertex_search_service.search_datastore(
            query=query,
            page_size=top_k,
            filter_expr=filter_expr
        )
        
        output = []
        for doc in res.documents:
            output.append({
                "id": doc.document_id,
                "title": doc.title,
                "content": doc.content,
                "uri": doc.uri,
                "score": doc.score,
                "metadata": doc.metadata
            })
        return output

# Singleton Retriever
vertex_retriever = VertexSearchRetriever()
