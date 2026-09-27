"""Cloud Storage Interface for RAG Documents and Evidence Artifacts"""
import os
import logging
from typing import List, Optional

logger = logging.getLogger(__name__)

class StorageService:
    def __init__(self, bucket_name: Optional[str] = None):
        self.bucket_name = bucket_name or os.getenv("GCS_BUCKET_NAME", "cardguard-knowledge-dev")
        self.local_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "knowledge"))

    async def list_knowledge_documents(self) -> List[str]:
        if os.path.exists(self.local_dir):
            return [f for f in os.listdir(self.local_dir) if f.endswith(".txt") or f.endswith(".pdf")]
        return []

    async def read_document(self, filename: str) -> str:
        filepath = os.path.join(self.local_dir, filename)
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                return f.read()
        raise FileNotFoundError(f"Document {filename} not found at {filepath}")

storage_service = StorageService()
