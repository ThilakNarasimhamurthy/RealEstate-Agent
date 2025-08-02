from app.core.mongo import db
from typing import Optional
from bson import ObjectId
from datetime import datetime
from app.services.mongo_user_service import MongoUserService

async def resolve_user_id(user_id: str):
    try:
        return ObjectId(user_id)
    except Exception:
        # Treat as email, look up or create user
        user = await MongoUserService.get_or_create_user_by_email(user_id)
        return user['_id']

class MongoConversationService:
    @staticmethod
    async def create_conversation(user_id: str):
        user_obj_id = await resolve_user_id(user_id)
        conversation = {
            "user_id": user_obj_id,
            "started_at": datetime.utcnow(),
        }
        result = await db.conversations.insert_one(conversation)
        conversation["_id"] = result.inserted_id
        return conversation

    @staticmethod
    async def get_conversation(conversation_id: str):
        try:
            return await db.conversations.find_one({"_id": ObjectId(conversation_id)})
        except Exception:
            return await db.conversations.find_one({"_id": conversation_id})

    @staticmethod
    async def list_conversations_for_user(user_id: str):
        user_obj_id = await resolve_user_id(user_id)
        return [conv async for conv in db.conversations.find({"user_id": user_obj_id})] 