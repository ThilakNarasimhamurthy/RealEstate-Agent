#!/usr/bin/env python3
"""
Document Ingestion Script for MongoDB Atlas Vector Search
Ingests uploaded documents into the RAG system
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the backend directory to Python path
sys.path.append(str(Path(__file__).parent))

from app.services.rag_service import ingest_document_to_mongodb
from app.core.mongo import db

async def ingest_uploaded_documents():
    """Ingest all documents in the uploads directory"""
    uploads_dir = Path("data/uploads")
    
    if not uploads_dir.exists():
        print("❌ Uploads directory not found")
        return
    
    files = list(uploads_dir.glob("*"))
    if not files:
        print("❌ No files found in uploads directory")
        return
    
    print(f"📁 Found {len(files)} files to ingest")
    
    total_ingested = 0
    for file_path in files:
        try:
            print(f"🔄 Ingesting {file_path.name}...")
            count = await ingest_document_to_mongodb(str(file_path))
            print(f"✅ Ingested {count} chunks from {file_path.name}")
            total_ingested += count
        except Exception as e:
            print(f"❌ Error ingesting {file_path.name}: {e}")
    
    print(f"\n🎉 Total chunks ingested: {total_ingested}")

async def test_vector_search():
    """Test vector search functionality"""
    from app.services.rag_service import vector_search_mongodb
    
    print("\n🔍 Testing vector search...")
    
    test_queries = [
        "office space downtown",
        "3 bedroom house suburban",
        "apartment with parking",
        "commercial property for rent"
    ]
    
    for query in test_queries:
        try:
            results = await vector_search_mongodb(query, k=3)
            print(f"✅ Query: '{query}' -> Found {len(results)} results")
            for i, result in enumerate(results[:2]):  # Show first 2 results
                print(f"   {i+1}. Score: {result.get('score', 'N/A'):.3f} - {result.get('text', '')[:100]}...")
        except Exception as e:
            print(f"❌ Error testing query '{query}': {e}")

async def main():
    """Main function"""
    print("🚀 Starting document ingestion...")
    
    # Check MongoDB connection
    if db is None:
        print("❌ MongoDB connection not available")
        return
    
    print("✅ MongoDB connection established")
    
    # Ingest documents
    await ingest_uploaded_documents()
    
    # Test vector search
    await test_vector_search()
    
    print("\n✨ Document ingestion complete!")

if __name__ == "__main__":
    asyncio.run(main()) 