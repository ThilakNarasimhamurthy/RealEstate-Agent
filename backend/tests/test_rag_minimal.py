#!/usr/bin/env python3
"""
Minimal test to isolate RAG server issue.
"""

import os
from dotenv import load_dotenv
load_dotenv()

print("Testing RAG server import and basic functionality...")

try:
    # Test just the import
    from app.mcp.servers.rag_server import RAGServer
    print("✅ RAGServer import successful")
    
    # Test instantiation
    rag = RAGServer()
    print("✅ RAGServer instantiation successful")
    
    # Test stats
    stats = rag.get_stats()
    print(f"✅ RAGServer stats: {stats}")
    
    # Test search (this is where the error occurs)
    try:
        results = rag.search_documents("test query")
        print(f"✅ RAGServer search successful: {len(results)} results")
    except Exception as e:
        print(f"❌ RAGServer search failed: {e}")
        print(f"Error type: {type(e).__name__}")
        
except Exception as e:
    print(f"❌ RAGServer test failed: {e}")
    print(f"Error type: {type(e).__name__}")
    import traceback
    traceback.print_exc() 