from fastapi import APIRouter, HTTPException
from typing import Optional
from app.services.mongo_user_service import MongoUserService
from app.services.mongo_conversation_service import MongoConversationService
from app.services.mongo_message_service import MongoMessageService

# Utility to fix ObjectId serialization

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

router = APIRouter(prefix="/mongo", tags=["mongo_chat"])

# User endpoints
@router.post("/users")
async def create_user(email: str, name: Optional[str] = None, company: Optional[str] = None):
    user = await MongoUserService.create_user(email, name, company)
    return fix_mongo_id(user)

@router.get("/users/by_email")
async def get_user_by_email(email: str):
    user = await MongoUserService.get_user_by_email(email)
    if not user:
        raise HTTPException(404, "User not found")
    return fix_mongo_id(user)

@router.get("/users/{user_id}")
async def get_user_by_id(user_id: str):
    user = await MongoUserService.get_user_by_id(user_id)
    if not user:
        raise HTTPException(404, "User not found")
    return fix_mongo_id(user)

@router.get("/users")
async def list_users():
    return fix_mongo_ids(await MongoUserService.list_users())

# Conversation endpoints
@router.post("/conversations")
async def create_conversation(user_id: str):
    conv = await MongoConversationService.create_conversation(user_id)
    return fix_mongo_id(conv)

@router.get("/conversations/{conv_id}")
async def get_conversation(conv_id: str):
    conv = await MongoConversationService.get_conversation(conv_id)
    if not conv:
        raise HTTPException(404, "Conversation not found")
    return fix_mongo_id(conv)

@router.get("/conversations/user/{user_id}")
async def list_conversations_for_user(user_id: str):
    return fix_mongo_ids(await MongoConversationService.list_conversations_for_user(user_id))

# Message endpoints
@router.post("/messages")
async def add_message(conversation_id: str, role: str, content: str):
    msg = await MongoMessageService.add_message(conversation_id, role, content)
    return fix_mongo_id(msg)

@router.get("/messages/{conversation_id}")
async def get_messages_for_conversation(conversation_id: str):
    return fix_mongo_ids(await MongoMessageService.get_messages_for_conversation(conversation_id)) 