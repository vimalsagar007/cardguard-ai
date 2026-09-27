#!/usr/bin/env python3
"""CARDGUARD AI v2.0 Test Runner (Pure Asyncio/Unittest)"""
import os
import sys
import asyncio
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services.document_ai_service import document_ai_service
from app.rag.advanced_rag import advanced_rag_engine
from app.decision_engine.engine import decision_engine

class TestCardGuardV2(unittest.IsolatedAsyncioTestCase):

    async def test_document_ai_receipt_basic(self):
        sample_text = b"RECEIPT: Paris Luxury Electronics\nTotal: $450.00\nDate: 2026-09-26"
        res = await document_ai_service.process_receipt(
            document_bytes=sample_text,
            expected_card_amount=450.00
        )
        self.assertEqual(res.processor_type, "RECEIPT_PROCESSOR")
        self.assertIsNotNone(res.vendor_name)
        self.assertFalse(res.discrepancy_flag)

    async def test_document_ai_receipt_discrepancy(self):
        sample_text = b"RECEIPT: Paris Luxury Electronics\nTotal: $12570.00\nDate: 2026-09-26"
        res = await document_ai_service.process_receipt(
            document_bytes=sample_text,
            expected_card_amount=12450.00
        )
        self.assertTrue(res.discrepancy_flag)
        self.assertIsNotNone(res.discrepancy_reason)

    async def test_expand_query(self):
        queries = await advanced_rag_engine.expand_query("international travel limit")
        self.assertEqual(len(queries), 3)
        self.assertIn("international travel limit", queries[0])

    async def test_generate_hypothetical_document(self):
        hyde_doc = await advanced_rag_engine.generate_hypothetical_document("electronics limit")
        self.assertTrue("electronics" in hyde_doc.lower() or "policy" in hyde_doc.lower())

    async def test_execute_advanced_rag(self):
        res = await advanced_rag_engine.execute_advanced_rag(
            query="international travel expense approval limit over 2500",
            top_k=3
        )
        self.assertEqual(res.original_query, "international travel expense approval limit over 2500")
        self.assertEqual(len(res.expanded_queries), 3)
        self.assertGreater(res.grounding_fidelity_score, 0.0)
        self.assertGreater(len(res.citations), 0)

    async def test_deterministic_decision_engine(self):
        tx = {"amount": 12450.00, "is_international": True, "merchant_country": "AE"}
        emp = {"single_tx_limit": 5000.00}
        merch = {"merchant_name": "Dubai Luxury", "is_high_risk_mcc": True, "merchant_category_code": "6051", "is_approved_vendor": False}
        
        assessment, decision, human_req, signals = decision_engine.evaluate(
            tx=tx, emp=emp, merch=merch, velocity_count=4, policy_violations=["POL-001"]
        )
        self.assertEqual(assessment.risk_level.value, "CRITICAL")
        self.assertTrue(assessment.total_risk_score >= 80.0)
        self.assertTrue(human_req)

if __name__ == "__main__":
    print("=" * 70)
    print("RUNNING CARDGUARD AI v2.0 SUITE (DOCUMENT AI & VERTEX RAG)")
    print("=" * 70)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCardGuardV2)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    if result.wasSuccessful():
        print("\n" + "=" * 70)
        print("ALL CARDGUARD AI v2.0 TESTS PASSED (100% SUCCESS)")
        print("=" * 70)
        sys.exit(0)
    else:
        sys.exit(1)
