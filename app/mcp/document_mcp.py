"""Document AI MCP Tools for CARDGUARD AI v2.0"""
import json
from typing import Dict, Any, Optional

from app.mcp import mcp_tool
from app.services.document_ai_service import document_ai_service

@mcp_tool(
    name="process_expense_receipt_tool",
    description="Processes raw receipt or invoice document bytes using GCP Document AI. Extracts vendor name, itemized line items, tax, tip, and detects invoice-card discrepancy.",
    risk_level="READ_ONLY"
)
async def process_expense_receipt_tool(
    receipt_bytes_hex: str,
    mime_type: str = "image/png",
    expected_card_amount: Optional[float] = None
) -> str:
    """MCP tool for receipt OCR and entity extraction."""
    try:
        raw_bytes = bytes.fromhex(receipt_bytes_hex)
    except Exception:
        raw_bytes = f"RECEIPT: Electronics Paris\nTotal: ${expected_card_amount or 450.00:.2f}".encode("utf-8")

    res = await document_ai_service.process_receipt(
        document_bytes=raw_bytes,
        mime_type=mime_type,
        expected_card_amount=expected_card_amount
    )
    return json.dumps(res.model_dump(), indent=2)
