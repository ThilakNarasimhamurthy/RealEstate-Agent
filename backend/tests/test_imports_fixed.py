#!/usr/bin/env python3
"""
Test script to verify all imports are working after restructuring.
"""

import sys
import os

# Add the backend directory to the Python path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

def test_all_imports():
    """Test all the key imports to ensure they work after restructuring."""
    
    print("🧪 Testing All Import Paths...")
    
    # Test 1: API imports
    print("1. Testing API imports...")
    try:
        from app.api import chat, crm, files
        print("   ✅ chat.py imports working")
        print("   ✅ crm.py imports working") 
        print("   ✅ files.py imports working")
    except ImportError as e:
        print(f"   ❌ Import failed: {e}")
        print(f"   Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
    
    # Test 2: MCP imports
    print("\n2. Testing MCP imports...")
    try:
        from app.mcp import MCPClientManager, MCPRegistry
        from app.mcp.servers import RAGServer, CRMServer
        from app.mcp.tools import DatabaseTools, LLMTools
        print("   ✅ MCP client and registry imports working")
        print("   ✅ MCP servers imports working")
        print("   ✅ MCP tools imports working")
    except ImportError as e:
        print(f"   ❌ Import failed: {e}")
        print(f"   Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
    
    # Test 3: Agents imports
    print("\n3. Testing Agents imports...")
    try:
        from app.agents import BaseAgent, OrchestratorAgent, AgentOrchestrator
        from app.agents.conversational import ChatAgent
        from app.agents.data import RAGAgent, CRMAgent
        print("   ✅ Base agent imports working")
        print("   ✅ Orchestrator imports working")
        print("   ✅ Chat agent imports working")
        print("   ✅ RAG agent imports working")
        print("   ✅ CRM agent imports working")
    except ImportError as e:
        print(f"   ❌ Import failed: {e}")
        print(f"   Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
    
    # Test 4: Core functionality imports
    print("\n4. Testing Core functionality imports...")
    try:
        from app.core.database import get_db
        from app.models import user, conversation, message
        from app.schemas import user as user_schemas
        print("   ✅ Database imports working")
        print("   ✅ Models imports working")
        print("   ✅ Schemas imports working")
    except ImportError as e:
        print(f"   ❌ Import failed: {e}")
        print(f"   Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
    
    # Test 5: Test actual functionality
    print("\n5. Testing actual functionality...")
    try:
        # Test MCP client creation
        from app.mcp import MCPClientManager
        client_manager = MCPClientManager()
        print("   ✅ MCP client manager creation working")
        
        # Test agent creation
        from app.agents import OrchestratorAgent
        orchestrator = OrchestratorAgent()
        print("   ✅ Orchestrator agent creation working")
        
        # Test RAG server creation
        from app.mcp.servers import RAGServer
        rag_server = RAGServer()
        print("   ✅ RAG server creation working")
        
        # Test CRM server creation
        from app.mcp.servers import CRMServer
        # Note: CRMServer needs a db_session, so we'll just test import
        print("   ✅ CRM server import working")
        
    except Exception as e:
        print(f"   ❌ Functionality test failed: {e}")
        print(f"   Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
    
    print("\n✅ All import tests completed!")

if __name__ == "__main__":
    test_all_imports() 