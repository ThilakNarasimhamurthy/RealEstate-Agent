#!/usr/bin/env python3
"""
Real Estate Chatbot Simulation Flow Test
Tests if the backend follows the expected conversation simulation
"""

import requests
import json
import time
from typing import Dict, Any, List
import sys

class SimulationTester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session_id: str = "test_user"
        self.conversation_id: str = ""
        self.test_results = []
        
    def log_test(self, test_name: str, success: bool, details: str = ""):
        """Log test results"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"   Details: {details}")
        self.test_results.append({
            "test": test_name,
            "success": success,
            "details": details
        })
        print()

    def test_api_health(self) -> bool:
        """Test if API is running"""
        try:
            response = requests.get(f"{self.base_url}/docs")
            return response.status_code == 200
        except Exception as e:
            return False

    def send_chat_message(self, message: str, session_id: str = "") -> Dict[str, Any]:
        """Send a chat message and return response"""
        payload = {
            "message": message,
            "user_id": session_id or self.session_id or "test_user"
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/chat",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    def test_session_1_initial_interaction(self):
        """Test Session 1: Initial User Interaction"""
        print("🔍 Testing Session 1: Initial User Interaction")
        print("=" * 50)

        # Test 1: First Message
        print("Testing API Call 1: First Message")
        response = self.send_chat_message(
            "Hi, I'm looking for office space in downtown area for my tech startup"
        )
        
        # Check response structure
        has_response = "response" in response
        has_session_id = "user_id" in response or "session_id" in response
        has_conversation_id = "conversation_id" in response
        
        self.log_test(
            "First message response structure",
            has_response and has_session_id and has_conversation_id,
            f"Response: {response.get('response', 'MISSING')[:100]}..."
        )
        
        # Store session and conversation IDs
        self.session_id = response.get("user_id") or response.get("session_id") or "test_user"
        self.conversation_id = response.get("conversation_id") or ""
        
        # Test 2: User Provides Details
        print("Testing API Call 2: User Provides Details")
        response2 = self.send_chat_message(
            "I'm Sarah Chen, and we need about 2000-3000 sq ft. Our budget is around $30-40 per sq ft annually",
            self.session_id
        )
        
        # Check for RAG sources and CRM data
        has_rag_sources = "rag_sources" in response2 or "sources" in response2
        has_crm_data = "crm_data_captured" in response2 or "extracted_info" in response2
        
        self.log_test(
            "Second message with RAG and CRM",
            has_rag_sources and has_crm_data,
            f"RAG sources: {response2.get('rag_sources', response2.get('sources', []))}, "
            f"CRM data: {response2.get('crm_data_captured', response2.get('extracted_info', {}))}"
        )
        
        # Test 3: Follow-up Question
        print("Testing API Call 3: Follow-up Question")
        response3 = self.send_chat_message(
            "The Tech Tower option sounds interesting. Can you tell me more about the building amenities and parking situation?",
            self.session_id
        )
        
        # Check for detailed property information
        response_text = response3.get("response", "")
        has_amenities = "amenities" in response_text.lower() or "parking" in response_text.lower()
        has_property_details = "tech tower" in response_text.lower()
        
        self.log_test(
            "Detailed property information",
            has_amenities and has_property_details,
            f"Response contains property details: {has_property_details}, amenities: {has_amenities}"
        )

    def test_session_2_return_conversation(self):
        """Test Session 2: Return Conversation"""
        print("🔍 Testing Session 2: Return Conversation")
        print("=" * 50)

        # Test 4: User Returns
        print("Testing API Call 4: User Returns")
        response4 = self.send_chat_message(
            "Hi, this is Sarah Chen again. I saw the Tech Tower space and loved it! What are the next steps?",
            self.session_id
        )
        
        # Check for context awareness
        response_text = response4.get("response", "")
        has_context = "sarah" in response_text.lower() or "tech tower" in response_text.lower()
        has_next_steps = "next steps" in response_text.lower() or "application" in response_text.lower()
        
        self.log_test(
            "Context awareness and next steps",
            has_context and has_next_steps,
            f"Context aware: {has_context}, Next steps: {has_next_steps}"
        )
        
        # Test 5: Contact Information Exchange
        print("Testing API Call 5: Contact Information Exchange")
        response5 = self.send_chat_message(
            "Perfect! My email is sarah.chen@innovatetech.startup. We'd prefer a 3-year lease with an option to expand if we grow. Also, do you have any other clients in the building we could potentially collaborate with?",
            self.session_id
        )
        
        # Check for email extraction and lease terms
        response_text = response5.get("response", "")
        has_email = "sarah.chen@innovatetech.startup" in response_text
        has_lease_terms = "3-year" in response_text or "lease" in response_text
        has_collaboration = "collaborate" in response_text or "tenants" in response_text
        
        self.log_test(
            "Contact info and lease discussion",
            has_email and has_lease_terms,
            f"Email captured: {has_email}, Lease terms: {has_lease_terms}, Collaboration: {has_collaboration}"
        )

    def test_crm_functionality(self):
        """Test CRM functionality"""
        print("🔍 Testing CRM Functionality")
        print("=" * 50)

        # Test CRM data capture
        print("Testing CRM data capture")
        response = self.send_chat_message(
            "Can you send me the application form? My company is InnovateTech and we're ready to move forward.",
            self.session_id
        )
        
        crm_data = response.get("crm_data_captured", response.get("extracted_info", {}))
        response_text = response.get("response", "")
        has_application = "application" in response_text.lower()
        has_company_mention = "innovatetech" in response_text.lower()
        
        self.log_test(
            "CRM data capture",
            has_application and has_company_mention,
            f"Company mentioned in response: {has_company_mention}, Application mentioned: {has_application}"
        )

    def test_rag_functionality(self):
        """Test RAG functionality"""
        print("🔍 Testing RAG Functionality")
        print("=" * 50)

        # Test property search
        print("Testing property search via RAG")
        response = self.send_chat_message(
            "Show me properties with 4+ bedrooms under $800k in suburban areas",
            self.session_id
        )
        
        rag_sources = response.get("rag_sources", response.get("sources", []))
        has_sources = len(rag_sources) > 0
        response_text = response.get("response", "")
        has_property_info = "property" in response_text.lower() or "bedroom" in response_text.lower()
        
        self.log_test(
            "RAG property search",
            has_sources and has_property_info,
            f"RAG sources: {len(rag_sources)}, Property info: {has_property_info}"
        )

    def test_analytics_endpoints(self):
        """Test analytics endpoints"""
        print("🔍 Testing Analytics Endpoints")
        print("=" * 50)

        try:
            # Test engagement analytics
            response = requests.get(f"{self.base_url}/analytics/user-engagement")
            has_engagement = response.status_code == 200
            
            self.log_test(
                "Engagement analytics endpoint",
                has_engagement,
                f"Status: {response.status_code}"
            )
            
            # Test conversation stats
            response = requests.get(f"{self.base_url}/analytics/conversation-stats")
            has_conversations = response.status_code == 200
            
            self.log_test(
                "Conversation analytics endpoint",
                has_conversations,
                f"Status: {response.status_code}"
            )
            
        except Exception as e:
            self.log_test(
                "Analytics endpoints",
                False,
                f"Error: {str(e)}"
            )

    def run_full_simulation_test(self):
        """Run the complete simulation test"""
        print("🚀 Starting Real Estate Chatbot Simulation Test")
        print("=" * 60)
        
        # Check API health
        if not self.test_api_health():
            print("❌ Backend API is not running. Please start the backend first.")
            return False
        
        print("✅ Backend API is running")
        print()
        
        # Run all test sessions
        self.test_session_1_initial_interaction()
        self.test_session_2_return_conversation()
        self.test_crm_functionality()
        self.test_rag_functionality()
        self.test_analytics_endpoints()
        
        # Summary
        print("📊 Test Summary")
        print("=" * 60)
        passed = sum(1 for result in self.test_results if result["success"])
        total = len(self.test_results)
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        if passed == total:
            print("\n🎉 All tests passed! Backend is following the simulation flow correctly.")
        else:
            print("\n⚠️  Some tests failed. Check the details above.")
        
        return passed == total

def main():
    """Main test runner"""
    tester = SimulationTester()
    success = tester.run_full_simulation_test()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 