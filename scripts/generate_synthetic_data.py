"""Synthetic Data Generator for CardGuard AI

Generates realistic synthetic datasets for testing:
- 100,000 Transactions (normal, borderline, fraudulent velocity, geo-anomaly, MCC risk)
- 1,000 Employees with departments and spending limits
- 5,000 Merchants with MCC codes, risk scores, and locations
- 100 Historical Fraud Cases
- 10 Enterprise Knowledge Documents in data/knowledge/ (.pdf or text)
"""

import os
import json
import random
from datetime import datetime, timedelta

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
KNOWLEDGE_DIR = os.path.join(DATA_DIR, "knowledge")

os.makedirs(os.path.join(DATA_DIR, "transactions"), exist_ok=True)
os.makedirs(os.path.join(DATA_DIR, "employees"), exist_ok=True)
os.makedirs(os.path.join(DATA_DIR, "merchants"), exist_ok=True)
os.makedirs(os.path.join(DATA_DIR, "cases"), exist_ok=True)
os.makedirs(KNOWLEDGE_DIR, exist_ok=True)

DEPARTMENTS = ["Engineering", "Sales", "Marketing", "Finance", "HR", "Legal", "Executive", "Operations"]
CITIES = [
    ("New York", "US"), ("San Francisco", "US"), ("London", "GB"), ("Tokyo", "JP"),
    ("Paris", "FR"), ("Singapore", "SG"), ("Sydney", "AU"), ("Dubai", "AE"),
    ("Zurich", "CH"), ("Frankfurt", "DE"), ("Toronto", "CA"), ("Sao Paulo", "BR")
]
MCC_CATEGORIES = {
    "5732": ("Electronics Stores", False, 15.0),
    "5812": ("Restaurants & Dining", False, 5.0),
    "3000": ("Airlines", False, 10.0),
    "7011": ("Hotels & Lodging", False, 10.0),
    "5944": ("Jewelry Stores", True, 65.0),
    "7995": ("Gambling & Casino", True, 90.0),
    "6051": ("Cryptocurrency & Wire Transfer", True, 95.0),
    "5541": ("Gas Stations", False, 12.0),
    "5311": ("Department Stores", False, 8.0)
}

def generate_employees(count=1000):
    print(f"Generating {count} synthetic employees...")
    employees = []
    first_names = ["Alex", "Jordan", "Taylor", "Morgan", "Sam", "Chris", "Pat", "Riley", "Casey", "Avery"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]
    
    for i in range(1, count + 1):
        emp_id = f"EMP-{i:05d}"
        fn = random.choice(first_names)
        ln = random.choice(last_names)
        dept = random.choice(DEPARTMENTS)
        
        limit = 5000.0
        if dept == "Executive":
            limit = 50000.0
        elif dept in ["Sales", "Marketing"]:
            limit = 15000.0
            
        emp = {
            "employee_id": emp_id,
            "full_name": f"{fn} {ln}",
            "email": f"{fn.lower()}.{ln.lower()}@corp-example.com",
            "department": dept,
            "title": f"Senior {dept} Specialist",
            "single_tx_limit": limit,
            "monthly_spending_limit": limit * 4,
            "historical_avg_tx_amount": round(random.uniform(50, 450), 2),
            "historical_fraud_cases_count": random.choices([0, 1, 2], weights=[0.95, 0.04, 0.01])[0],
            "corporate_card_id": f"CARD-{random.randint(1000, 9999)}"
        }
        employees.append(emp)
        
    path = os.path.join(DATA_DIR, "employees", "employees.json")
    with open(path, "w") as f:
        json.dump(employees, f, indent=2)
    print(f"Saved employees to {path}")
    return employees

def generate_merchants(count=5000):
    print(f"Generating {count} synthetic merchants...")
    merchants = []
    merchant_prefixes = ["Apex", "Global", "City", "Summit", "Prime", "Starlight", "Vanguard", "Horizon", "Metro", "Royal"]
    merchant_suffixes = ["Services", "Tech", "Holdings", "Group", "Boutique", "Outlet", "Club", "Resort", "Mart", "Express"]
    
    mcc_keys = list(MCC_CATEGORIES.keys())
    
    for i in range(1, count + 1):
        m_id = f"MERCH-{i:05d}"
        mcc = random.choice(mcc_keys)
        mcc_desc, is_high_risk, base_risk = MCC_CATEGORIES[mcc]
        name = f"{random.choice(merchant_prefixes)} {random.choice(merchant_suffixes)}"
        city, country = random.choice(CITIES)
        
        # Add risk variance
        risk_score = min(100.0, max(0.0, base_risk + random.gauss(0, 10)))
        
        merch = {
            "merchant_id": m_id,
            "merchant_name": name,
            "merchant_category_code": mcc,
            "mcc_description": mcc_desc,
            "city": city,
            "country": country,
            "is_high_risk_mcc": is_high_risk,
            "risk_score": round(risk_score, 1),
            "historical_chargeback_rate": round(random.uniform(0.01, 3.5 if is_high_risk else 0.5), 2),
            "is_approved_vendor": random.choices([True, False], weights=[0.2, 0.8])[0]
        }
        merchants.append(merch)
        
    path = os.path.join(DATA_DIR, "merchants", "merchants.json")
    with open(path, "w") as f:
        json.dump(merchants, f, indent=2)
    print(f"Saved merchants to {path}")
    return merchants

def generate_transactions(employees, merchants, count=100000):
    print(f"Generating {count} synthetic transactions...")
    transactions = []
    base_time = datetime.utcnow() - timedelta(days=30)
    
    # Pre-select some explicit fraud pattern targets
    fraud_employees = random.sample(employees, 50)
    
    for i in range(1, count + 1):
        tx_id = f"TXN-{i:08d}"
        
        # 3% chance of being explicitly flagged synthetic fraud pattern
        is_fraud_scenario = (i % 30 == 0)
        
        if is_fraud_scenario:
            emp = random.choice(fraud_employees)
            merch = random.choice([m for m in merchants if m["is_high_risk_mcc"]])
            amount = round(random.uniform(emp["single_tx_limit"] * 1.2, emp["single_tx_limit"] * 4.0), 2)
            city, country = ("Dubai", "AE") if random.random() > 0.5 else ("Zurich", "CH")
            is_intl = True
        else:
            emp = random.choice(employees)
            merch = random.choice(merchants)
            amount = round(random.uniform(5.0, emp["single_tx_limit"] * 0.8), 2)
            city, country = merch["city"], merch["country"]
            is_intl = (country != "US")
            
        time_offset = random.randint(0, 30 * 86400)
        tx_time = base_time + timedelta(seconds=time_offset)
        
        tx = {
            "transaction_id": tx_id,
            "card_id": emp["corporate_card_id"],
            "employee_id": emp["employee_id"],
            "merchant_id": merch["merchant_id"],
            "merchant_name": merch["merchant_name"],
            "merchant_category_code": merch["merchant_category_code"],
            "merchant_country": country,
            "amount": amount,
            "currency": "USD",
            "timestamp": tx_time.isoformat(),
            "location_city": city,
            "location_country": country,
            "pos_entry_mode": "ECOMMERCE" if is_intl else "CHIP",
            "is_international": is_intl,
            "is_synthetic_fraud": is_fraud_scenario
        }
        transactions.append(tx)
        
    path = os.path.join(DATA_DIR, "transactions", "transactions.json")
    with open(path, "w") as f:
        json.dump(transactions[:5000], f, indent=2) # Save subset in JSON for fast local dev testing
    print(f"Saved sample transactions to {path} (Full set: {len(transactions)})")
    
    # Save a CSV for BigQuery loading
    import csv
    csv_path = os.path.join(DATA_DIR, "transactions", "transactions.csv")
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=transactions[0].keys())
        writer.writeheader()
        writer.writerows(transactions)
    print(f"Saved CSV transactions to {csv_path}")
    return transactions

def generate_cases(transactions, count=100):
    print(f"Generating {count} synthetic fraud cases...")
    cases = []
    fraud_txs = [t for t in transactions if t.get("is_synthetic_fraud")]
    if len(fraud_txs) < count:
        fraud_txs = transactions[:count]
        
    for i in range(1, count + 1):
        tx = fraud_txs[i - 1]
        c_id = f"CASE-{i:05d}"
        
        case = {
            "case_id": c_id,
            "transaction_id": tx["transaction_id"],
            "status": random.choice(["OPEN", "IN_INVESTIGATION", "PENDING_APPROVAL", "CLOSED"]),
            "created_at": tx["timestamp"],
            "updated_at": tx["timestamp"],
            "assigned_reviewer": f"analyst_{random.randint(1, 10)}@corp-example.com",
            "risk_level": random.choice(["HIGH", "CRITICAL"]),
            "risk_score": round(random.uniform(65.0, 98.0), 1),
            "investigation_summary": f"Synthetic fraud investigation for high amount transaction ${tx['amount']} at {tx['merchant_name']}.",
            "decision": random.choice(["ESCALATE", "BLOCK_PENDING_APPROVAL"]),
            "timeline": [
                {"timestamp": tx["timestamp"], "event": "Real-time anomaly detected by CardGuard AI", "actor": "SYSTEM"},
                {"timestamp": tx["timestamp"], "event": "Investigation case created automatically", "actor": "case_agent"}
            ]
        }
        cases.append(case)
        
    path = os.path.join(DATA_DIR, "cases", "cases.json")
    with open(path, "w") as f:
        json.dump(cases, f, indent=2)
    print(f"Saved cases to {path}")
    return cases

def generate_knowledge_documents():
    print("Generating synthetic policy knowledge documents...")
    docs = {
        "corporate_card_policy.pdf": """# Corporate Card Usage Policy (Version 2026.1)
Effective Date: January 1, 2026
Document ID: POL-CORP-CARD-2026

1. Purpose and Scope
This policy governs the issuance and usage of corporate credit cards issued to employees of Example Enterprise Inc.

2. Permissible Expenses
2.1 Corporate cards must strictly be used for legitimate business expenses, including travel, business dining, software subscriptions, and authorized client entertainment.
2.2 Personal expenses of any kind are strictly prohibited on corporate cards.

3. Transaction Limits and Approvals
3.1 Single Transaction Limit: Standard employees have a single transaction limit of $5,000 USD. Department heads have a $15,000 USD limit. Executive committee members have a $50,000 USD limit.
3.2 Any single expense exceeding the assigned limit requires prior written pre-approval from the Department Finance Director.
3.3 Splitting transactions to circumvent single transaction limits is a severe violation resulting in card suspension.

4. High-Risk Merchant Categories
4.1 Corporate cards are restricted from being used at Gambling & Casino merchants (MCC 7995), Cryptocurrency & Wire Transfers (MCC 6051), and Adult Entertainment.
4.2 Purchases at Jewelry Stores (MCC 5944) exceeding $1,000 USD require prior pre-authorization.
""",
        "travel_policy.pdf": """# Global Business Travel Policy (Version 2026.2)
Effective Date: February 15, 2026
Document ID: POL-TRAVEL-2026

1. Air Travel Guidelines
1.1 All domestic and international flights must be booked through the approved corporate travel portal.
1.2 Economy class is mandatory for domestic flights under 5 hours. Premium Economy or Business Class is permitted for international flights over 8 hours with VP approval.

2. Hotel & Lodging
2.1 Maximum allowable daily lodging rate is $350 USD for tier-1 cities (New York, London, Tokyo, San Francisco) and $250 USD for all other locations.
2.2 Expenses exceeding lodging ceilings require exception authorization.

3. Meal Allowances & Dining
3.1 Daily meal allowance (Per Diem) is $100 USD in tier-1 cities and $75 USD elsewhere.
3.2 Group business dining over $500 USD must list all employee and client attendees.
""",
        "expense_policy.pdf": """# Employee Expense Reimbursement Policy (Version 2025.4)
Effective Date: October 1, 2025
Document ID: POL-EXP-2025

1. Receipt Requirements
1.1 Itemized receipts are mandatory for all card charges over $25 USD.
1.2 Receipts must show date, merchant name, individual line items, tax, and tip.

2. Submission Timeline
2.1 All corporate card transactions must be reconciled and submitted within 15 calendar days of the statement period end date.
""",
        "merchant_policy.pdf": """# Merchant Risk & Vendor Approval Policy (Version 2026.1)
Effective Date: January 10, 2026
Document ID: POL-MERCH-2026

1. High-Risk Merchants
1.1 Merchants with chargeback rates exceeding 2.0% or risk scores above 75.0 are classified as High-Risk Merchants.
1.2 Transactions at High-Risk Merchants require multi-agent fraud investigation and automated risk scoring.
""",
        "international_transaction_policy.pdf": """# International & Cross-Border Card Usage Policy
Effective Date: March 1, 2026
Document ID: POL-INTL-2026

1. Cross-Border Controls
1.1 International transactions conducted in countries outside the employee's assigned home region must be accompanied by an active Travel Request Notification in the system.
1.2 Unannounced cross-border transactions over $1,000 USD conducted within 2 hours of a home-country transaction trigger automated geographic velocity anomaly alerts.
""",
        "fraud_investigation_sop.pdf": """# Standard Operating Procedure: Corporate Card Fraud Investigation (SOP-808)
Effective Date: January 1, 2026
Document ID: SOP-FRAUD-808

1. Overview
This SOP defines the multi-agent investigation workflow for corporate card anomalies.

2. Triaging Anomaly Signals
2.1 When velocity, amount, or geographic jump signals fire, the Supervisor Agent must delegate tasks to Fraud, Policy, Merchant, Employee, and Case sub-agents.
2.2 Every claim generated in an investigation report must cite specific policy clauses or transaction log records.
""",
        "fraud_escalation_policy.pdf": """# Fraud Escalation & Human-In-The-Loop Approval Policy
Effective Date: January 1, 2026
Document ID: POL-ESCALATE-2026

1. Risk Score Thresholds
1.1 Risk Score < 30.0: CLEAR. Transaction cleared automatically.
1.2 30.0 <= Risk Score < 60.0: MONITOR. Transaction flagged for post-clearing audit.
1.3 60.0 <= Risk Score < 85.0: ESCALATE. Assigned to human analyst for review.
1.4 Risk Score >= 85.0 or Policy Violation: BLOCK_PENDING_APPROVAL. Card block pending explicit human approval.
""",
        "employee_expense_policy.pdf": """# Employee Conduct & Cardholder Agreement
Effective Date: January 1, 2026
Document ID: POL-EMP-AGREEMENT-2026

1. Cardholder Responsibilities
1.1 Employees are personally accountable for all charges incurred on their assigned corporate card.
""",
        "historical_fraud_cases.pdf": """# Historical Fraud Patterns & Case Studies (2025 Archive)
Document ID: ARCHIVE-FRAUD-2025

Case CS-2025-01: Split Transaction Evasion
Employee attempted to purchase $12,000 software license by running four $3,000 charges within 10 minutes at the same vendor to bypass the $5,000 single transaction limit.

Case CS-2025-02: Geographic Impossible Velocity
Card used at gas station in Chicago at 14:00, and 45 minutes later used at high-end luxury retail in Paris at 14:45. Confirmed stolen card clone.
""",
        "approved_merchants.pdf": """# Approved Corporate Vendor & Merchant Directory
Document ID: DIR-APPROVED-MERCH-2026

Approved Airline Vendors: Delta Air Lines, United Airlines, British Airways, Lufthansa, Singapore Airlines.
Approved Hotel Vendors: Marriott, Hilton, Hyatt, InterContinental, Accor.
Approved Tech Vendors: AWS, Google Cloud, Microsoft, Apple Store, CDW, SHI.
"""
    }

    for filename, text in docs.items():
        path = os.path.join(KNOWLEDGE_DIR, filename)
        # Save as text file (or formatted mock PDF text file)
        # To make it compatible with both PDF reader and text parser, save as text file / md / pdf
        text_filename = filename.replace(".pdf", ".txt")
        text_path = os.path.join(KNOWLEDGE_DIR, text_filename)
        with open(text_path, "w") as f:
            f.write(text)
        print(f"Saved knowledge document {text_path}")

if __name__ == "__main__":
    employees = generate_employees(1000)
    merchants = generate_merchants(5000)
    transactions = generate_transactions(employees, merchants, 100000)
    cases = generate_cases(transactions, 100)
    generate_knowledge_documents()
    print("Synthetic data generation completed successfully!")
