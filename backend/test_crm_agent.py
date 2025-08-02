#!/usr/bin/env python3
"""
Test CRMAgent methods
"""

import asyncio
import sys
import os

async def test_crm_agent():
    """Test CRMAgent methods"""
    try:
        from app.agents.data.crm_agent import CRMAgent
        
        print("Testing CRMAgent...")
        
        # Create CRMAgent instance
        crm_agent = CRMAgent()
        
        # Test if methods exist
        print(f"Has get_or_create_user: {hasattr(crm_agent, 'get_or_create_user')}")
        print(f"Has extract_user_info: {hasattr(crm_agent, 'extract_user_info')}")
        
        # Test extract_user_info
        test_message = "Hi, I'm John from Acme Corp, my email is john@acme.com"
        extracted_info = crm_agent.extract_user_info(test_message)
        print(f"Extracted info: {extracted_info}")
        
        # Test get_or_create_user (this might fail due to MongoDB connection)
        try:
            user_info = {"email": "test@example.com", "name": "Test User"}
            user = await crm_agent.get_or_create_user(user_info)
            print(f"User created/retrieved: {user}")
        except Exception as e:
            print(f"get_or_create_user failed: {e}")
            
        print("✅ CRMAgent test completed!")
        return True
        
    except Exception as e:
        print(f"❌ CRMAgent test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    result = asyncio.run(test_crm_agent())
    sys.exit(0 if result else 1) 