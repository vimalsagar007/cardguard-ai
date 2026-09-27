"""BigQuery Service Interface with Local In-Memory / File Fallback"""
import os
import json
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class BigQueryService:
    def __init__(self, project_id: Optional[str] = None, dataset_id: Optional[str] = None):
        self.project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT", "cardguard-dev")
        self.dataset_id = dataset_id or os.getenv("BIGQUERY_DATASET", "cardguard_fraud_db")
        self._use_gcp = False
        self._in_memory_tx: Dict[str, Dict[str, Any]] = {}
        self._in_memory_employees: Dict[str, Dict[str, Any]] = {}
        self._in_memory_merchants: Dict[str, Dict[str, Any]] = {}
        self._in_memory_cases: Dict[str, Dict[str, Any]] = {}
        
        # Load local JSON datasets into memory for fast fallback queries
        self._load_local_data()

    def _load_local_data(self):
        data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data"))
        
        # Transactions
        tx_path = os.path.join(data_dir, "transactions", "transactions.json")
        if os.path.exists(tx_path):
            with open(tx_path) as f:
                txs = json.load(f)
                for tx in txs:
                    self._in_memory_tx[tx["transaction_id"]] = tx
                    
        # Employees
        emp_path = os.path.join(data_dir, "employees", "employees.json")
        if os.path.exists(emp_path):
            with open(emp_path) as f:
                emps = json.load(f)
                for emp in emps:
                    self._in_memory_employees[emp["employee_id"]] = emp

        # Merchants
        merch_path = os.path.join(data_dir, "merchants", "merchants.json")
        if os.path.exists(merch_path):
            with open(merch_path) as f:
                merchs = json.load(f)
                for m in merchs:
                    self._in_memory_merchants[m["merchant_id"]] = m

        # Cases
        case_path = os.path.join(data_dir, "cases", "cases.json")
        if os.path.exists(case_path):
            with open(case_path) as f:
                cases = json.load(f)
                for c in cases:
                    self._in_memory_cases[c["case_id"]] = c

        logger.info(f"Loaded in-memory datasets: {len(self._in_memory_tx)} transactions, {len(self._in_memory_employees)} employees, {len(self._in_memory_merchants)} merchants, {len(self._in_memory_cases)} cases.")

    async def get_transaction(self, transaction_id: str) -> Optional[Dict[str, Any]]:
        return self._in_memory_tx.get(transaction_id)

    async def query_card_velocity(self, card_id: str, minutes_window: int = 60) -> List[Dict[str, Any]]:
        """Calculates transaction velocity for a card within the specified minutes window."""
        results = [tx for tx in self._in_memory_tx.values() if tx["card_id"] == card_id]
        results.sort(key=lambda x: x["timestamp"], reverse=True)
        return results[:10]

    async def get_employee(self, employee_id: str) -> Optional[Dict[str, Any]]:
        return self._in_memory_employees.get(employee_id)

    async def get_merchant(self, merchant_id: str) -> Optional[Dict[str, Any]]:
        return self._in_memory_merchants.get(merchant_id)

    async def get_case(self, case_id: str) -> Optional[Dict[str, Any]]:
        return self._in_memory_cases.get(case_id)

    async def save_case(self, case_data: Dict[str, Any]) -> str:
        case_id = case_data["case_id"]
        self._in_memory_cases[case_id] = case_data
        return case_id

bq_service = BigQueryService()
