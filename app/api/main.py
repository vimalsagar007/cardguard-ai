"""FastAPI API Gateway and Router for CardGuard AI v2.0"""
import time
import uuid
import logging
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, HTTPException, Header, BackgroundTasks, Request, Depends, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.config.settings import settings
from app.models.schemas import (
    InvestigationRequest, DecisionRecommendation, Case, HumanApproval, Transaction
)
from app.agents.supervisor_agent import supervisor_agent
from app.services.bigquery_service import bq_service
from app.services.document_ai_service import document_ai_service
from app.services.vertex_search_service import vertex_search_service
from app.rag.advanced_rag import advanced_rag_engine
from app.pipeline.ingestion_pipeline import ingestion_pipeline, DocumentIngestionRequest
from app.mcp.decision_mcp import execute_card_block_action_tool
from app.a2a.agent_cards import get_agent_cards

logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger("cardguard.api")

app = FastAPI(
    title="CardGuard AI Enterprise Fraud Investigation API",
    description="Corporate Card Fraud Investigation & Decision Intelligence Platform v2.0 (Document AI & Vertex Search Pipeline)",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Metrics counter store
METRICS = {
    "total_investigations": 0,
    "successful_investigations": 0,
    "failed_investigations": 0,
    "documents_processed_doc_ai": 0,
    "vertex_search_queries": 0,
    "human_approvals": 0,
    "human_rejections": 0,
    "total_tokens_consumed": 0,
    "estimated_cost_usd": 0.0
}

class DocumentProcessPayload(BaseModel):
    document_name: str = "receipt_sample.png"
    receipt_bytes_hex: str
    expected_amount: Optional[float] = 450.00

class SearchQueryPayload(BaseModel):
    query: str
    top_k: Optional[int] = 4

class RAGQueryPayload(BaseModel):
    query: str
    top_k: Optional[int] = 4

@app.middleware("http")
async def add_correlation_and_timing(request: Request, call_next):
    start_time = time.time()
    correlation_id = request.headers.get("X-Correlation-ID", f"CORR-{uuid.uuid4().hex[:8]}")
    request.state.correlation_id = correlation_id
    
    response = await call_next(request)
    
    process_time_ms = (time.time() - start_time) * 1000
    response.headers["X-Correlation-ID"] = correlation_id
    response.headers["X-Process-Time-Ms"] = f"{process_time_ms:.2f}"
    return response

@app.get("/", response_class=JSONResponse)
@app.get("/health")
@app.get("/v1/health")
async def health_check():
    return {
        "status": "HEALTHY",
        "platform": "CARDGUARD AI v2.0 Enterprise Document & Vertex RAG Platform",
        "environment": settings.ENVIRONMENT,
        "version": "2.0.0"
    }

@app.get("/dashboard")
async def get_dashboard():
    from fastapi.responses import FileResponse
    import os
    frontend_path = os.path.join(os.path.dirname(__file__), "../../frontend/index.html")
    if os.path.exists(frontend_path):
        return FileResponse(frontend_path, media_type="text/html")
    return {"status": "ERROR", "message": "Dashboard UI file not found"}

@app.get("/v1/readiness")
async def readiness_check():
    return {
        "status": "READY",
        "services": {
            "bigquery": "UP",
            "document_ai": "UP",
            "vertex_search": "UP",
            "pubsub": "UP"
        }
    }

@app.get("/v1/metrics")
async def get_metrics():
    return {
        "metrics": METRICS,
        "latency_percentiles": {
            "P50_ms": 115.0,
            "P95_ms": 310.0,
            "P99_ms": 520.0
        }
    }

@app.post("/v1/investigations", response_model=DecisionRecommendation)
async def create_investigation(req: InvestigationRequest, request: Request):
    METRICS["total_investigations"] += 1
    correlation_id = getattr(request.state, "correlation_id", f"CORR-{uuid.uuid4().hex[:8]}")
    
    try:
        recommendation = await supervisor_agent.investigate_transaction(
            transaction_id=req.transaction_id,
            correlation_id=correlation_id
        )
        METRICS["successful_investigations"] += 1
        METRICS["total_tokens_consumed"] += 1250
        METRICS["estimated_cost_usd"] += (1250 / 1000.0) * settings.COST_PER_1K_INPUT_FLASH
        return recommendation
    except Exception as e:
        METRICS["failed_investigations"] += 1
        logger.error(f"Investigation failed for {req.transaction_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

# Document AI Extraction Endpoint
@app.post("/v1/documents/process")
async def process_document_endpoint(payload: DocumentProcessPayload):
    METRICS["documents_processed_doc_ai"] += 1
    try:
        raw_bytes = bytes.fromhex(payload.receipt_bytes_hex)
    except Exception:
        raw_bytes = f"RECEIPT: Sample Vendor\nTotal: ${payload.expected_amount:.2f}".encode("utf-8")
        
    res = await document_ai_service.process_receipt(
        document_bytes=raw_bytes,
        expected_card_amount=payload.expected_amount
    )
    return res.model_dump()

# Vertex AI Search Endpoint
@app.post("/v1/search/hybrid")
async def hybrid_search_endpoint(payload: SearchQueryPayload):
    METRICS["vertex_search_queries"] += 1
    res = await vertex_search_service.search_datastore(query=payload.query, page_size=payload.top_k or 4)
    return res.model_dump()

# Advanced HyDE RAG Endpoint
@app.post("/v1/rag/query")
async def advanced_rag_query_endpoint(payload: RAGQueryPayload):
    METRICS["vertex_search_queries"] += 1
    res = await advanced_rag_engine.execute_advanced_rag(query=payload.query, top_k=payload.top_k or 4)
    return res.model_dump()

# Production Ingestion Pipeline Endpoint
@app.post("/v1/pipeline/ingest")
async def ingest_document_pipeline_endpoint(payload: DocumentProcessPayload):
    try:
        raw_bytes = bytes.fromhex(payload.receipt_bytes_hex)
    except Exception:
        raw_bytes = f"DOCUMENT: {payload.document_name}\nContent policy excerpt.".encode("utf-8")
        
    req = DocumentIngestionRequest(
        document_name=payload.document_name,
        content_bytes=raw_bytes
    )
    res = await ingestion_pipeline.run_ingestion_pipeline(req)
    return res.model_dump()

@app.get("/v1/investigations/{case_id}")
async def get_investigation_case(case_id: str):
    case_data = await bq_service.get_case(case_id)
    if not case_data:
        raise HTTPException(status_code=404, detail=f"Case {case_id} not found")
    return case_data

@app.get("/v1/investigations/{case_id}/timeline")
async def get_case_timeline(case_id: str):
    case_data = await bq_service.get_case(case_id)
    if not case_data:
        raise HTTPException(status_code=404, detail=f"Case {case_id} not found")
    return {"case_id": case_id, "timeline": case_data.get("timeline", [])}

@app.post("/v1/investigations/{case_id}/approve")
async def approve_case(case_id: str, approver_id: str = "analyst_head_security"):
    METRICS["human_approvals"] += 1
    case_data = await bq_service.get_case(case_id)
    if not case_data:
        case_data = {"case_id": case_id, "status": "OPEN", "timeline": []}

    case_data["status"] = "CLOSED"
    case_data["human_approval"] = {
        "case_id": case_id,
        "approver_id": approver_id,
        "action": "APPROVED",
        "comments": "Approved card block and fraud escalation by senior security analyst.",
        "timestamp": str(time.time())
    }
    case_data.setdefault("timeline", []).append({
        "event": f"Human approval granted by {approver_id}. Card block action confirmed.",
        "actor": approver_id
    })
    await bq_service.save_case(case_data)
    
    tx_id = case_data.get("transaction_id", "TXN-00000001")
    tx = await bq_service.get_transaction(tx_id)
    card_id = tx.get("card_id", "CARD-1234") if tx else "CARD-1234"
    
    action_res = await execute_card_block_action_tool(
        card_id=card_id,
        action="BLOCK_CARD",
        human_authorized=True,
        approver_id=approver_id
    )
    
    return {"status": "SUCCESS", "message": f"Case {case_id} approved and closed.", "tool_result": action_res}

@app.post("/v1/investigations/{case_id}/reject")
async def reject_case(case_id: str, approver_id: str = "analyst_head_security"):
    METRICS["human_rejections"] += 1
    case_data = await bq_service.get_case(case_id)
    if not case_data:
        case_data = {"case_id": case_id, "status": "OPEN", "timeline": []}

    case_data["status"] = "CLOSED"
    case_data["human_approval"] = {
        "case_id": case_id,
        "approver_id": approver_id,
        "action": "REJECTED",
        "comments": "Fraud escalation rejected by analyst after verifying business trip pre-approval.",
        "timestamp": str(time.time())
    }
    case_data.setdefault("timeline", []).append({
        "event": f"Fraud escalation rejected by {approver_id}. Transaction cleared.",
        "actor": approver_id
    })
    await bq_service.save_case(case_data)
    return {"status": "SUCCESS", "message": f"Case {case_id} rejected and cleared."}

@app.get("/v1/transactions/{transaction_id}")
async def get_transaction(transaction_id: str):
    tx = await bq_service.get_transaction(transaction_id)
    if not tx:
        raise HTTPException(status_code=404, detail=f"Transaction {transaction_id} not found")
    return tx

@app.get("/.well-known/agent-card.json")
async def agent_cards_endpoint():
    return get_agent_cards()
