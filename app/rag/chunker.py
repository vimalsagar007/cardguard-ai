"""Semantic and Fallback Document Chunking for Policy RAG"""
import re
from typing import List, Dict, Any

class DocumentChunk:
    def __init__(self, chunk_id: str, document_name: str, section_title: str, text: str, metadata: Dict[str, Any]):
        self.chunk_id = chunk_id
        self.document_name = document_name
        self.section_title = section_title
        self.text = text
        self.metadata = metadata

class PolicyChunker:
    def __init__(self, target_chunk_size: int = 500, overlap: int = 100):
        self.target_chunk_size = target_chunk_size
        self.overlap = overlap

    def chunk_document(self, document_name: str, text: str) -> List[DocumentChunk]:
        """Performs semantic section chunking with recursive fallback."""
        chunks: List[DocumentChunk] = []
        
        # Split by section headers (# or 1. or 2.1)
        sections = re.split(r'\n(?=#+|\d+\.\s|\d+\.\d+\s)', text)
        
        chunk_idx = 0
        for section in sections:
            section_str = section.strip()
            if not section_str:
                continue
                
            # Extract header if present
            lines = section_str.split('\n')
            first_line = lines[0].strip()
            section_title = first_line if re.match(r'#+|\d+\.', first_line) else "General Policy"
            
            # If section is small enough, keep as single chunk
            if len(section_str) <= self.target_chunk_size * 2:
                chunk_id = f"{document_name}#chunk_{chunk_idx}"
                chunks.append(DocumentChunk(
                    chunk_id=chunk_id,
                    document_name=document_name,
                    section_title=section_title,
                    text=section_str,
                    metadata={
                        "document_name": document_name,
                        "effective_date": "2026-01-01",
                        "version": "v1.0"
                    }
                ))
                chunk_idx += 1
            else:
                # Fallback recursive chunking for long sections
                sub_chunks = self._recursive_chunk(section_str)
                for sub in sub_chunks:
                    chunk_id = f"{document_name}#chunk_{chunk_idx}"
                    chunks.append(DocumentChunk(
                        chunk_id=chunk_id,
                        document_name=document_name,
                        section_title=section_title,
                        text=sub,
                        metadata={
                            "document_name": document_name,
                            "effective_date": "2026-01-01",
                            "version": "v1.0"
                        }
                    ))
                    chunk_idx += 1
                    
        return chunks

    def _recursive_chunk(self, text: str) -> List[str]:
        words = text.split()
        chunks = []
        start = 0
        while start < len(words):
            end = start + self.target_chunk_size
            chunk_words = words[start:end]
            chunks.append(" ".join(chunk_words))
            start += (self.target_chunk_size - self.overlap)
        return chunks

policy_chunker = PolicyChunker()
