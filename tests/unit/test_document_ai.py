"""Unit Tests for Document AI Service & Receipt OCR Entity Extraction"""
import pytest
from app.services.document_ai_service import document_ai_service

@pytest.mark.asyncio
async def test_process_receipt_basic():
    sample_text = b"RECEIPT: Paris Luxury Electronics\nTotal: $450.00\nDate: 2026-09-26"
    res = await document_ai_service.process_receipt(
        document_bytes=sample_text,
        expected_card_amount=450.00
    )
    assert res.processor_type == "RECEIPT_PROCESSOR"
    assert res.vendor_name is not None
    assert res.discrepancy_flag is False

@pytest.mark.asyncio
async def test_process_receipt_discrepancy():
    sample_text = b"RECEIPT: Paris Luxury Electronics\nTotal: $12570.00\nDate: 2026-09-26"
    res = await document_ai_service.process_receipt(
        document_bytes=sample_text,
        expected_card_amount=12450.00
    )
    assert res.discrepancy_flag is True
    assert "exceeds" in res.discrepancy_reason or "does not match" in res.discrepancy_reason
