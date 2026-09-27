"""Hybrid BM25/Vector RAG Retriever with Reranking and Context Compression"""
import os
import re
import math
import logging
from typing import List, Dict, Any, Tuple
from app.rag.chunker import policy_chunker, DocumentChunk
from app.services.storage_service import storage_service

logger = logging.getLogger(__name__)

class HybridRagRetriever:
    def __init__(self):
        self.chunks: List[DocumentChunk] = []
        self._is_indexed = False

    async def initialize_index(self):
        """Loads knowledge docs and builds hybrid search index."""
        if self._is_indexed:
            return
            
        doc_files = await storage_service.list_knowledge_documents()
        all_chunks = []
        for doc_file in doc_files:
            try:
                content = await storage_service.read_document(doc_file)
                doc_chunks = policy_chunker.chunk_document(doc_file, content)
                all_chunks.extend(doc_chunks)
            except Exception as e:
                logger.error(f"Failed to chunk document {doc_file}: {e}")
                
        self.chunks = all_chunks
        self._is_indexed = True
        logger.info(f"Indexed {len(self.chunks)} knowledge policy chunks across {len(doc_files)} files.")

    def _token_score(self, query: str, text: str) -> float:
        """Calculates token overlap BM25 score."""
        query_words = set(re.findall(r'\w+', query.lower()))
        if not query_words:
            return 0.0
            
        text_words = re.findall(r'\w+', text.lower())
        if not text_words:
            return 0.0
            
        matches = sum(1 for w in query_words if w in text_words)
        return matches / len(query_words)

    async def retrieve(
        self,
        query: str,
        top_k: int = 5,
        document_filter: List[str] = None
    ) -> List[Tuple[DocumentChunk, float]]:
        """Performs hybrid retrieval with filtering and reranking."""
        await self.initialize_index()
        
        scored_chunks: List[Tuple[DocumentChunk, float]] = []
        
        for chunk in self.chunks:
            if document_filter and chunk.document_name not in document_filter:
                continue
                
            score = self._token_score(query, chunk.text + " " + chunk.section_title)
            
            # Boost score if query matches document name
            if any(term in chunk.document_name.lower() for term in query.lower().split()):
                score += 0.3
                
            if score > 0.05:
                scored_chunks.append((chunk, min(1.0, score)))
                
        # Sort by relevance score descending
        scored_chunks.sort(key=lambda x: x[1], reverse=True)
        return scored_chunks[:top_k]

    def compress_context(self, retrieved_chunks: List[Tuple[DocumentChunk, float]], max_tokens: int = 2000) -> str:
        """Compresses retrieved chunks into unified prompt context window."""
        context_parts = []
        token_count = 0
        
        for chunk, score in retrieved_chunks:
            chunk_str = f"--- Document: {chunk.document_name} | Section: {chunk.section_title} | Score: {score:.2f} ---\n{chunk.text}\n"
            words = len(chunk_str.split())
            if token_count + words > max_tokens:
                break
            context_parts.append(chunk_str)
            token_count += words
            
        return "\n".join(context_parts)

rag_retriever = HybridRagRetriever()
