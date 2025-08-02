from app.core.mongo import db
from typing import Dict, List, Optional
import openai
import os
from datetime import datetime, timedelta

class CRMService:
    def __init__(self):
        self.openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    async def extract_user_info(self, message: str, user_id: str) -> Dict:
        """
        Extract user information from messages using AI
        """
        prompt = f"""
        Extract the following information from this message: "{message}"
        
        Return as JSON with these fields:
        - name (if mentioned)
        - email (if mentioned)
        - phone (if mentioned)
        - budget (if mentioned)
        - property_type (house, condo, etc.)
        - location_preference (if mentioned)
        - timeline (when they want to buy/sell)
        - urgency (high, medium, low)
        """
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200
            )
            # Parse the response (in production, you'd want better JSON parsing)
            extracted_info = {
                "name": None,
                "email": None,
                "phone": None,
                "budget": None,
                "property_type": None,
                "location_preference": None,
                "timeline": None,
                "urgency": "medium"
            }
            
            # Simple keyword extraction for demo
            message_lower = message.lower()
            if "house" in message_lower or "home" in message_lower:
                extracted_info["property_type"] = "house"
            if "condo" in message_lower:
                extracted_info["property_type"] = "condo"
            if "downtown" in message_lower:
                extracted_info["location_preference"] = "downtown"
            if "suburban" in message_lower:
                extracted_info["location_preference"] = "suburban"
            
            return extracted_info
            
        except Exception as e:
            return {"error": str(e)}
    
    async def create_lead(self, user_id: str, extracted_info: Dict) -> Dict:
        """
        Create a new lead in the CRM
        """
        lead = {
            "user_id": user_id,
            "extracted_info": extracted_info,
            "status": "new",
            "created_at": datetime.utcnow(),
            "last_contact": datetime.utcnow(),
            "notes": [],
            "follow_up_date": datetime.utcnow() + timedelta(days=1)
        }
        
        result = await db.leads.insert_one(lead)
        lead["_id"] = result.inserted_id
        return lead
    
    async def update_lead(self, lead_id: str, updates: Dict) -> Dict:
        """
        Update lead information
        """
        updates["last_contact"] = datetime.utcnow()
        result = await db.leads.update_one(
            {"_id": lead_id},
            {"$set": updates}
        )
        return {"updated": result.modified_count > 0}
    
    async def add_note_to_lead(self, lead_id: str, note: str) -> Dict:
        """
        Add a note to a lead
        """
        note_entry = {
            "content": note,
            "created_at": datetime.utcnow()
        }
        
        result = await db.leads.update_one(
            {"_id": lead_id},
            {"$push": {"notes": note_entry}}
        )
        return {"added": result.modified_count > 0}
    
    async def get_leads_by_user(self, user_id: str) -> List[Dict]:
        """
        Get all leads for a user
        """
        return [lead async for lead in db.leads.find({"user_id": user_id})]
    
    async def get_leads_needing_followup(self) -> List[Dict]:
        """
        Get leads that need follow-up
        """
        today = datetime.utcnow()
        return [lead async for lead in db.leads.find({
            "follow_up_date": {"$lte": today},
            "status": {"$ne": "closed"}
        })]
    
    async def schedule_followup(self, lead_id: str, days_from_now: int = 1) -> Dict:
        """
        Schedule a follow-up for a lead
        """
        follow_up_date = datetime.utcnow() + timedelta(days=days_from_now)
        result = await db.leads.update_one(
            {"_id": lead_id},
            {"$set": {"follow_up_date": follow_up_date}}
        )
        return {"scheduled": result.modified_count > 0} 