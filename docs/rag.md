# CardGuard AI RAG Architecture

## Hybrid Retrieval & Grounding Pipeline
1. **Document Knowledge Base**: 10 synthetic enterprise policies stored in `data/knowledge/`.
2. **Chunking**: Semantic section headers (`#` / `1.1`) combined with recursive token fallback chunking.
3. **Hybrid Search**: BM25 keyword matching combined with vector similarity search.
4. **Context Compression**: Dynamic prompt context window trimming to maximize relevance while controlling token cost.
5. **Grounding Verifier**: 8-step claim verification ensuring all policy findings cite valid document clauses. Rejects ungrounded claims with `"Evidence unavailable; unable to verify this claim."`
