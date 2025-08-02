from fastapi import APIRouter, Query
from app.services.analytics_service import AnalyticsService
from typing import Optional

router = APIRouter(prefix="/analytics", tags=["analytics"])
analytics_service = AnalyticsService()

@router.get("/rag-metrics")
async def rag_metrics():
    return await analytics_service.get_rag_metrics()

@router.get("/crm-insights")
async def crm_insights():
    return await analytics_service.get_crm_insights()

@router.get("/lead-scores")
async def lead_scores():
    return await analytics_service.get_lead_scores()

@router.get("/conversation-stats")
async def conversation_stats(user_id: Optional[str] = Query(None)):
    return await analytics_service.get_conversation_stats(user_id)

@router.get("/user-engagement")
async def user_engagement(days: int = Query(30)):
    return await analytics_service.get_user_engagement(days) 