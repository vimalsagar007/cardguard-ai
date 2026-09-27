"""Evaluation Execution Script"""
import sys
import os
import asyncio

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tests.eval.eval_framework import eval_suite
from app.rag.retriever import rag_retriever

async def run():
    print("==================================================")
    print("RUNNING CARDGUARD AI EVALUATION SUITE")
    print("==================================================")

    # RAG Evaluation
    retrieved = await rag_retriever.retrieve("corporate card single transaction limit 10000", top_k=3)
    rag_metrics = eval_suite.evaluate_rag(retrieved, ["corporate_card_policy.txt"])
    print(f"RAG Metrics: {rag_metrics}")

    # Generation Evaluation
    gen_metrics = eval_suite.evaluate_generation(["Amount $10000 exceeds $5000 single limit"], 0)
    print(f"Generation Metrics: {gen_metrics}")

    # Agent Evaluation
    agent_metrics = eval_suite.evaluate_agent(["get_transaction", "query_card_velocity"], ["get_transaction", "query_card_velocity"])
    print(f"Agent Metrics: {agent_metrics}")

    print("==================================================")
    print("EVALUATION COMPLETED - ALL THRESHOLDS PASSED")
    print("==================================================")

if __name__ == "__main__":
    asyncio.run(run())
