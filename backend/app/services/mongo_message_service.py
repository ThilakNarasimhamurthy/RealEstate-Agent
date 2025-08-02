from app.core.mongo import db
from typing import Optional
from bson import ObjectId
from datetime import datetime

class MongoMessageService:
    @staticmethod
    async def add_message(conversation_id: str, role: str, content: str):
        message = {
            "conversation_id": ObjectId(conversation_id),
            "role": role,
            "content": content,
            "created_at": datetime.utcnow(),
        }
        result = await db.messages.insert_one(message)
        message["_id"] = result.inserted_id
        return message

    @staticmethod
    async def get_messages_for_conversation(conversation_id: str):
        return [msg async for msg in db.messages.find({"conversation_id": ObjectId(conversation_id)})] 