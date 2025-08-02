from app.core.mongo import db
from typing import Optional
from bson import ObjectId
from datetime import datetime

class MongoUserService:
    @staticmethod
    async def create_user(email: str, name: Optional[str] = None, company: Optional[str] = None):
        user = {
            "email": email,
            "name": name,
            "company": company,
        }
        result = await db.users.insert_one(user)
        user["_id"] = result.inserted_id
        return user

    @staticmethod
    async def get_user_by_email(email: str):
        return await db.users.find_one({"email": email})

    @staticmethod
    async def get_user_by_id(user_id: str):
        try:
            return await db.users.find_one({"_id": ObjectId(user_id)})
        except Exception:
            return await db.users.find_one({"_id": user_id})

    @staticmethod
    async def get_or_create_user_by_email(email: str):
        user = await db.users.find_one({"email": email})
        if user:
            return user
        # Create new user
        new_user = {"email": email, "created_at": datetime.utcnow()}
        result = await db.users.insert_one(new_user)
        new_user["_id"] = result.inserted_id
        new_user["created"] = True
        return new_user

    @staticmethod
    async def list_users():
        return [user async for user in db.users.find({})]

    @staticmethod
    async def update_user(user_id: str, update_data: dict):
        await db.users.update_one({"_id": ObjectId(user_id)}, {"$set": update_data}) 