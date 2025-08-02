#!/usr/bin/env python3
"""
Test MongoDB connection and MongoUserService
"""

import asyncio
import sys
import os

async def test_mongo_connection():
    """Test MongoDB connection and basic operations"""
    try:
        from app.services.mongo_user_service import MongoUserService
        from app.core.mongo import db
        
        print("Testing MongoDB connection...")
        
        # Test if we can connect to MongoDB
        if db is None:
            print("❌ MongoDB connection failed - db is None")
            return False
            
        print("✅ MongoDB connection established")
        
        # Test MongoUserService
        user_service = MongoUserService()
        
        # Test creating a user
        print("Testing user creation...")
        test_email = "test@example.com"
        test_name = "Test User"
        test_company = "Test Company"
        
        user = await user_service.create_user(test_email, test_name, test_company)
        if user:
            print(f"✅ User created successfully: {user}")
        else:
            print("❌ User creation failed")
            return False
            
        # Test retrieving the user
        print("Testing user retrieval...")
        retrieved_user = await user_service.get_user_by_email(test_email)
        if retrieved_user:
            print(f"✅ User retrieved successfully: {retrieved_user}")
        else:
            print("❌ User retrieval failed")
            return False
            
        # Test updating the user
        print("Testing user update...")
        update_result = await user_service.update_user(str(retrieved_user["_id"]), {"name": "Updated Test User"})
        if update_result:
            print("✅ User updated successfully")
        else:
            print("❌ User update failed")
            
        print("✅ All MongoDB tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ MongoDB test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    result = asyncio.run(test_mongo_connection())
    sys.exit(0 if result else 1) 