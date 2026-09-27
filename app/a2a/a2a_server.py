"""A2A Server and Task Router Interface"""
import logging
from typing import Dict, Any
from pydantic import BaseModel
from app.a2a.agent_cards import get_agent_cards

logger = logging.getLogger(__name__)

class A2ATaskRequest(BaseModel):
    task_id: str
    target_agent: str
    correlation_id: str
    trace_id: str
    input_data: Dict[str, Any]

class A2ATaskResponse(BaseModel):
    task_id: str
    target_agent: str
    status: str = "COMPLETED"
    correlation_id: str
    trace_id: str
    output_data: Dict[str, Any]

class A2AServer:
    def __init__(self):
        self.cards = get_agent_cards()

    async def handle_task(self, request: A2ATaskRequest) -> A2ATaskResponse:
        logger.info(f"[A2A PROTOCOL] Task {request.task_id} dispatched to {request.target_agent} (Correlation: {request.correlation_id})")
        # Route to appropriate specialist agent
        return A2ATaskResponse(
            task_id=request.task_id,
            target_agent=request.target_agent,
            status="COMPLETED",
            correlation_id=request.correlation_id,
            trace_id=request.trace_id,
            output_data={"message": f"Task processed by {request.target_agent}", "received": request.input_data}
        )

a2a_server = A2AServer()
