from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import logging

# MCP Integration - FIXED import path
from app.agents.orchestrator import AgentOrchestrator 

router = APIRouter()
logger = logging.getLogger(__name__)

class ChatRequest(BaseModel):
    message: str
    user_id: Optional[str] = None
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    user_id: str
    session_id: Optional[str] = None  # Alias for user_id
    conversation_id: Optional[str] = None
    timestamp: datetime
    processing_time: float
    mcp_enabled: bool = True
    extracted_info: Optional[dict] = None
    rag_sources: Optional[list] = []
    sources: Optional[list] = []  # Alias for rag_sources
    crm_actions: Optional[list] = []
    crm_context: Optional[dict] = None
    crm_data_captured: Optional[dict] = None  # Merged extracted_info and crm_context
    properties: Optional[list] = []
    conversation_history: Optional[list] = []
    metadata: Optional[dict] = None

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Chat endpoint using MCP orchestrator - handles RAG + CRM + AI response
    """
    start_time = datetime.utcnow()
    
    try:
        logger.info(f"Processing chat request: {request.message[:50]}...")
        
        # Initialize MCP orchestrator
        orchestrator = AgentOrchestrator()
        
        # Generate user_id if not provided
        user_id = request.user_id or f"user_{int(datetime.utcnow().timestamp())}"
        
        # Process through MCP architecture
        result = await orchestrator.process_chat_request(
            message=request.message,
            user_id=user_id,
            conversation_id=request.conversation_id
        )
        response = result["response"]
        user_id = result.get("user_id", user_id)
        session_id = user_id  # Alias
        conversation_id = result.get("conversation_id", request.conversation_id)
        extracted_info = result.get("extracted_info")
        rag_sources = result.get("rag_sources", [])
        sources = rag_sources  # Alias
        crm_actions = result.get("crm_actions", [])
        crm_context = result.get("crm_context")
        # Merge extracted_info and crm_context for crm_data_captured
        crm_data_captured = {}
        if crm_context:
            crm_data_captured.update(crm_context)
        if extracted_info:
            crm_data_captured.update(extracted_info)
        properties = result.get("properties", [])
        conversation_history = result.get("conversation_history", [])
        metadata = result.get("metadata")
        
        # Calculate processing time
        processing_time = (datetime.utcnow() - start_time).total_seconds()
        
        logger.info(f"Chat processed successfully in {processing_time:.2f}s")
        
        return ChatResponse(
            response=response,
            user_id=user_id,
            session_id=session_id,
            conversation_id=conversation_id,
            timestamp=datetime.utcnow(),
            processing_time=processing_time,
            mcp_enabled=True,
            extracted_info=extracted_info,
            rag_sources=rag_sources,
            sources=sources,
            crm_actions=crm_actions,
            crm_context=crm_context,
            crm_data_captured=crm_data_captured,
            properties=properties,
            conversation_history=conversation_history,
            metadata=metadata
        )
        
    except Exception as e:
        processing_time = (datetime.utcnow() - start_time).total_seconds()
        logger.error(f"Chat processing failed after {processing_time:.2f}s: {str(e)}")
        
        raise HTTPException(
            status_code=500, 
            detail={
                "error": "Chat processing failed",
                "message": str(e),
                "processing_time": processing_time,
                "mcp_enabled": True
            }
        )

# Health check endpoint for MCP system
@router.get("/chat/health")
async def chat_health_check():
    """Health check for MCP chat system"""
    try:
        orchestrator = AgentOrchestrator()
        
        agent_status = {
            "rag_agent": "available" if orchestrator.rag_agent else "unavailable",
            "crm_agent": "available" if orchestrator.crm_agent else "unavailable", 
            "chat_agent": "available" if orchestrator.chat_agent else "unavailable",
            "total_agents": len(orchestrator.agents)
        }
        
        return {
            "status": "healthy",
            "mcp_enabled": True,
            "agents": agent_status,
            "timestamp": datetime.utcnow()
        }
        
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "mcp_enabled": False,
            "timestamp": datetime.utcnow()
        }