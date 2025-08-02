from app.core.mongo import db
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from collections import Counter

class AnalyticsService:
    
    async def get_conversation_stats(self, user_id: Optional[str] = None) -> Dict:
        # Get all conversation IDs (optionally filtered by user)
        query = {}
        if user_id:
            query["user_id"] = user_id
        conversation_ids = [c["_id"] for c in await db.conversations.find(query, {"_id": 1}).to_list(1000)]  # type: ignore[attr-defined]
        if not conversation_ids:
            return {"total_conversations": 0, "avg_messages_per_conversation": 0}
        # Count messages per conversation
        pipeline = [
            {"$match": {"conversation_id": {"$in": [str(cid) for cid in conversation_ids]}}},
            {"$group": {"_id": "$conversation_id", "count": {"$sum": 1}}}
        ]
        msg_counts = await db.messages.aggregate(pipeline).to_list(1000)  # type: ignore[attr-defined]
        total_conversations = len(conversation_ids)
        avg_messages = sum(m["count"] for m in msg_counts) / total_conversations if total_conversations else 0
        return {"total_conversations": total_conversations, "avg_messages_per_conversation": avg_messages}
    
    async def get_user_engagement(self, days: int = 30) -> Dict:
        """
        Get user engagement metrics
        """
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Active users
        active_users = await db.conversations.distinct("user_id", {
            "started_at": {"$gte": start_date}
        })  # type: ignore[attr-defined]
        
        # Total messages
        total_messages = await db.messages.count_documents({
            "created_at": {"$gte": start_date}
        })  # type: ignore[attr-defined]
        
        # New users
        new_users = await db.users.count_documents({
            "created_at": {"$gte": start_date}
        })  # type: ignore[attr-defined]
        
        return {
            "active_users": len(active_users),
            "total_messages": total_messages,
            "new_users": new_users,
            "period_days": days
        }
    
    async def get_rag_metrics(self) -> Dict:
        # Demo: count of RAG retrievals and average latency (mocked)
        rag_logs = await db.rag_logs.find({"timestamp": {"$gte": datetime.utcnow() - timedelta(days=7)}}).to_list(1000)  # type: ignore[attr-defined]
        retrieval_count = len(rag_logs)
        avg_latency = sum(log.get("latency", 0) for log in rag_logs) / retrieval_count if retrieval_count else 0
        return {"retrieval_count": retrieval_count, "avg_latency": avg_latency}

    async def get_crm_insights(self) -> Dict:
        user_count = await db.users.count_documents({})  # type: ignore[attr-defined]
        lead_count = await db.leads.count_documents({})  # type: ignore[attr-defined]
        return {"user_count": user_count, "lead_count": lead_count}

    async def get_lead_scores(self) -> List[Dict]:
        # WARNING: This is a mock/stub implementation. Replace with real lead scoring logic.
        # TODO: Implement real lead scoring analytics.
        leads = await db.leads.find({}).to_list(100)  # type: ignore[attr-defined]
        for lead in leads:
            lead["score"] = 80  # Placeholder
        return leads
    
    async def get_lead_conversion_stats(self) -> Dict:
        """
        Get lead conversion statistics
        """
        pipeline = [
            {"$group": {
                "_id": "$status",
                "count": {"$sum": 1}
            }}
        ]
        
        results = await db.leads.aggregate(pipeline).to_list(None)  # type: ignore[attr-defined]
        
        status_counts = {result["_id"]: result["count"] for result in results}
        
        total_leads = sum(status_counts.values())
        conversion_rate = (status_counts.get("closed", 0) / total_leads * 100) if total_leads > 0 else 0
        
        return {
            "total_leads": total_leads,
            "status_breakdown": status_counts,
            "conversion_rate": round(conversion_rate, 2)
        }
    
    async def get_property_search_trends(self) -> Dict:
        """
        Get property search trends and popular criteria
        WARNING: This is a mock/stub implementation. Replace with real analytics.
        TODO: Implement real property search trends analytics.
        """
        # Mock data for demo - in production, this would analyze actual search queries
        trends = {
            "popular_locations": ["Downtown", "Suburban", "Waterfront"],
            "popular_property_types": ["Single Family", "Condo", "Townhouse"],
            "price_ranges": {
                "300k-500k": 45,
                "500k-750k": 30,
                "750k+": 25
            },
            "bedroom_preferences": {
                "2": 20,
                "3": 50,
                "4+": 30
            }
        }
        return trends
    
    async def get_user_journey_insights(self, user_id: str) -> Dict:
        """
        Get insights about a specific user's journey
        """
        # Get user's conversations
        conversations = await db.conversations.find({"user_id": user_id}).to_list(None)  # type: ignore[attr-defined]
        
        # Get user's messages
        conversation_ids = [conv["_id"] for conv in conversations]
        messages = await db.messages.find({
            "conversation_id": {"$in": conversation_ids}
        }).to_list(None)  # type: ignore[attr-defined]
        
        # Get user's leads
        leads = await db.leads.find({"user_id": user_id}).to_list(None)  # type: ignore[attr-defined]
        
        # Analyze message patterns
        user_messages = [msg for msg in messages if msg["role"] == "user"]
        assistant_messages = [msg for msg in messages if msg["role"] == "assistant"]
        
        # Extract common topics (simple keyword analysis)
        user_text = " ".join([msg["content"].lower() for msg in user_messages])
        topics = []
        
        if "house" in user_text or "home" in user_text:
            topics.append("Property Search")
        if "price" in user_text or "budget" in user_text:
            topics.append("Pricing")
        if "location" in user_text or "area" in user_text:
            topics.append("Location")
        if "schedule" in user_text or "viewing" in user_text:
            topics.append("Viewings")
        
        return {
            "total_conversations": len(conversations),
            "total_messages": len(messages),
            "user_messages": len(user_messages),
            "assistant_messages": len(assistant_messages),
            "total_leads": len(leads),
            "active_leads": len([lead for lead in leads if lead.get("status") != "closed"]),
            "common_topics": topics,
            "engagement_score": min(100, len(messages) * 10)  # Simple scoring
        }
    
    async def get_daily_activity(self, days: int = 7) -> List[Dict]:
        """
        Get daily activity for the last N days
        """
        activities = []
        
        for i in range(days):
            date = datetime.utcnow() - timedelta(days=i)
            start_of_day = date.replace(hour=0, minute=0, second=0, microsecond=0)
            end_of_day = start_of_day + timedelta(days=1)
            
            # Count conversations started
            conversations = await db.conversations.count_documents({
                "started_at": {"$gte": start_of_day, "$lt": end_of_day}
            })  # type: ignore[attr-defined]
            
            # Count messages sent
            messages = await db.messages.count_documents({
                "created_at": {"$gte": start_of_day, "$lt": end_of_day}
            })  # type: ignore[attr-defined]
            
            # Count new leads
            leads = await db.leads.count_documents({
                "created_at": {"$gte": start_of_day, "$lt": end_of_day}
            })  # type: ignore[attr-defined]
            
            activities.append({
                "date": start_of_day.strftime("%Y-%m-%d"),
                "conversations": conversations,
                "messages": messages,
                "leads": leads
            })
        
        return activities[::-1]  # Reverse to show oldest first 