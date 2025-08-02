from fastapi import APIRouter, HTTPException, status
from app.services.mongo_user_service import MongoUserService
from app.services.mongo_conversation_service import MongoConversationService
from app.services.mongo_message_service import MongoMessageService
from app.schemas import user as user_s
from typing import List

router = APIRouter(prefix="/crm", tags=["crm"])

# POST /crm/create_user
@router.post("/create_user", response_model=user_s.UserOut, status_code=status.HTTP_201_CREATED)
async def create_user_ep(payload: user_s.UserCreate):
    existing = await MongoUserService.get_user_by_email(payload.email)
    if existing:
        raise HTTPException(400, "email already exists")
    user = await MongoUserService.create_user(payload.email, payload.name, payload.company)
    user["id"] = str(user["_id"])
    return user

# PUT /crm/update_user
@router.put("/update_user/{user_id}", response_model=user_s.UserOut)
async def update_user_ep(user_id: str, payload: user_s.UserUpdate):
    user = await MongoUserService.get_user_by_id(user_id)
    if not user:
        raise HTTPException(404, "user not found")
    update_data = {}
    if payload.name is not None:
        update_data["name"] = payload.name
    if payload.company is not None:
        update_data["company"] = payload.company
    if update_data:
        await MongoUserService.update_user(user_id, update_data)
        user.update(update_data)
    user["id"] = str(user["_id"])
    return user

# GET /crm/conversations/{user_id}   (list conversation IDs for user)
@router.get("/conversations/{user_id}", response_model=List[str])
async def list_conversations_ep(user_id: str):
    conversations = await MongoConversationService.list_conversations_for_user(user_id)
    return [str(conv["_id"]) for conv in conversations]