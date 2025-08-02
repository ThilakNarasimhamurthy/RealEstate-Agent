from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel
from typing import Optional, List, Dict
from app.services.rag_service import RAGService
from app.services.crm_service import CRMService
from app.services.analytics_service import AnalyticsService
from app.services.mongo_message_service import MongoMessageService
from app.services.mongo_conversation_service import MongoConversationService
from datetime import datetime
from app.core.mongo import db

router = APIRouter(prefix="/advanced", tags=["advanced_features"])

# Initialize services
rag_service = RAGService()
crm_service = CRMService()
analytics_service = AnalyticsService()

# Utility function to fix MongoDB ObjectId serialization
def fix_mongo_id(doc):
    if not doc:
        return doc
    doc = dict(doc)
    if "_id" in doc:
        doc["_id"] = str(doc["_id"])
    if "user_id" in doc and hasattr(doc["user_id"], "__str__"):
        doc["user_id"] = str(doc["user_id"])
    if "conversation_id" in doc and hasattr(doc["conversation_id"], "__str__"):
        doc["conversation_id"] = str(doc["conversation_id"])
    return doc

def fix_mongo_ids(docs):
    return [fix_mongo_id(doc) for doc in docs]

# RAG Endpoints
@router.get("/properties/search")
async def search_properties(query: str, limit: int = 5):
    """Search for properties based on user query"""
    properties = await rag_service.search_properties(query, limit)
    return {"query": query, "properties": fix_mongo_ids(properties)}

@router.get("/properties/{property_id}")
async def get_property_details(property_id: str):
    """Get detailed information about a specific property"""
    property_details = await rag_service.get_property_details(property_id)
    if not property_details:
        raise HTTPException(404, "Property not found")
    return fix_mongo_id(property_details)

@router.post("/properties/generate-response")
async def generate_property_response(query: str):
    """Generate AI response about properties"""
    properties = await rag_service.search_properties(query)
    response = await rag_service.generate_property_response(query, properties)
    return {"query": query, "response": response, "properties_found": len(properties)}

# CRM Endpoints
@router.post("/leads/extract-info")
async def extract_user_info(message: str, user_id: str):
    """Extract user information from message"""
    extracted_info = await crm_service.extract_user_info(message, user_id)
    return {"user_id": user_id, "extracted_info": extracted_info}

@router.post("/leads/create")
async def create_lead(user_id: str, extracted_info: dict):
    """Create a new lead"""
    lead = await crm_service.create_lead(user_id, extracted_info)
    return fix_mongo_id(lead)

@router.get("/leads/user/{user_id}")
async def get_leads_by_user(user_id: str):
    """Get all leads for a user"""
    leads = await crm_service.get_leads_by_user(user_id)
    return fix_mongo_ids(leads)

@router.get("/leads/followup")
async def get_leads_needing_followup():
    """Get leads that need follow-up"""
    leads = await crm_service.get_leads_needing_followup()
    return fix_mongo_ids(leads)

@router.put("/leads/{lead_id}")
async def update_lead(lead_id: str, updates: dict):
    """Update lead information"""
    result = await crm_service.update_lead(lead_id, updates)
    return result

@router.post("/leads/{lead_id}/notes")
async def add_note_to_lead(lead_id: str, note: str):
    """Add a note to a lead"""
    result = await crm_service.add_note_to_lead(lead_id, note)
    return result

@router.post("/leads/{lead_id}/schedule-followup")
async def schedule_followup(lead_id: str, days_from_now: int = 1):
    """Schedule a follow-up for a lead"""
    result = await crm_service.schedule_followup(lead_id, days_from_now)
    return result

# Analytics Endpoints
@router.get("/analytics/conversation-stats")
async def get_conversation_stats(user_id: Optional[str] = None):
    """Get conversation statistics"""
    stats = await analytics_service.get_conversation_stats(user_id)
    return stats

@router.get("/analytics/user-engagement")
async def get_user_engagement(days: int = 30):
    """Get user engagement metrics"""
    engagement = await analytics_service.get_user_engagement(days)
    return engagement

@router.get("/analytics/lead-conversion")
async def get_lead_conversion_stats():
    """Get lead conversion statistics"""
    stats = await analytics_service.get_lead_conversion_stats()
    return stats

@router.get("/analytics/property-trends")
async def get_property_search_trends():
    """Get property search trends"""
    trends = await analytics_service.get_property_search_trends()
    return trends

@router.get("/analytics/user-journey/{user_id}")
async def get_user_journey_insights(user_id: str):
    """Get insights about a specific user's journey"""
    insights = await analytics_service.get_user_journey_insights(user_id)
    return insights

@router.get("/analytics/daily-activity")
async def get_daily_activity(days: int = 7):
    """Get daily activity for the last N days"""
    activity = await analytics_service.get_daily_activity(days)
    return activity

class SmartChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    user_id: Optional[str] = None
    conversation_id: Optional[str] = None

class SmartChatResponse(BaseModel):
    response: str
    session_id: str
    sources: List[str]
    response_time: float
    conversation_id: str
    crm_data_captured: Dict
    properties_found: int

# Combined Chat with RAG and CRM
@router.post("/smart-chat", response_model=SmartChatResponse)
async def smart_chat_endpoint(request: SmartChatRequest):
    import time
    start = time.time()
    
    # 1. Generate or use session_id and user_id
    if not request.session_id:
        session_id = f"session_{int(time.time())}"
    else:
        session_id = request.session_id
    
    if not request.user_id:
        user_id = f"user_{int(time.time())}"
    else:
        user_id = request.user_id
    
    conversation_id = request.conversation_id

    # 2. Extract CRM info
    extracted_info = await crm_service.extract_user_info(request.message, user_id)

    # 3. RAG property search
    properties = await rag_service.search_properties(request.message)
    sources = [p.get("id", p.get("property_id", "")) for p in properties] if properties else []

    # 4. Generate AI response
    ai_response = await rag_service.generate_property_response(request.message, properties)

    # 5. Conversation management - use string IDs instead of ObjectId
    if not conversation_id:
        # Create conversation with string user_id
        conv = {
            "user_id": user_id,  # Use string, not ObjectId
            "started_at": datetime.utcnow(),
        }
        result = await db.conversations.insert_one(conv)
        conversation_id = str(result.inserted_id)

    # 6. Save messages - use string conversation_id
    user_msg = {
        "conversation_id": conversation_id,  # Use string, not ObjectId
        "role": "user",
        "content": request.message,
        "created_at": datetime.utcnow(),
    }
    await db.messages.insert_one(user_msg)
    
    assistant_msg = {
        "conversation_id": conversation_id,  # Use string, not ObjectId
        "role": "assistant", 
        "content": ai_response,
        "created_at": datetime.utcnow(),
    }
    await db.messages.insert_one(assistant_msg)

    # 7. CRM lead management
    leads = await crm_service.get_leads_by_user(user_id)
    if not leads:
        await crm_service.create_lead(user_id, extracted_info)

    # 8. Compose CRM data for response
    crm_data_captured = extracted_info or {}
    if properties:
        crm_data_captured["properties_found"] = len(properties)
        crm_data_captured["property_ids"] = sources

    # 9. Response time
    response_time = round(time.time() - start, 2)

    return SmartChatResponse(
        response=ai_response,
        session_id=session_id,
        sources=sources,
        response_time=response_time,
        conversation_id=conversation_id,
        crm_data_captured=crm_data_captured,
        properties_found=len(properties)
    ) 