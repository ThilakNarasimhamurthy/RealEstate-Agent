from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.mongo import db
from typing import List, Dict, Optional
import openai
import os
from datetime import datetime
import numpy as np
import csv

# Helper: chunk text (reuse your tokenizer logic as needed)
def simple_chunk_text(text: str, chunk_size: int = 500) -> list:
    # Simple whitespace chunking for demo; replace with tokenizer-based chunking for production
    words = text.split()
    return [' '.join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

async def ingest_document_to_mongodb(file_path: str, collection_name: str = "rag_chunks"):
    """
    Ingest a document: chunk, embed, and store in MongoDB Atlas for vector search.
    Supports .txt and .csv files.
    """
    if db is None:
        raise RuntimeError("MongoDB connection is not initialized. Check your MONGO_URI.")
    import openai
    import os
    openai.api_key = os.getenv("OPENAI_API_KEY")
    docs = []
    if file_path.lower().endswith('.csv'):
        # Read CSV and treat each row as a chunk
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                # Concatenate all fields for a rich text chunk
                chunk = ", ".join(f"{k}: {v}" for k, v in row.items() if v and k.lower() not in {"", "id", "unique_id"})
                if not chunk.strip():
                    continue
                resp = openai.embeddings.create(model="text-embedding-3-small", input=[chunk])
                embedding = resp.data[0].embedding
                doc = {
                    "text": chunk,
                    "embedding": embedding,
                    "file": os.path.basename(file_path),
                    "chunk_id": i,
                    "created_at": datetime.utcnow(),
                    "metadata": row
                }
                docs.append(doc)
    else:
        # Read file
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
        
        chunks = simple_chunk_text(text)
        for i, chunk in enumerate(chunks):
            # Get embedding from OpenAI
            resp = openai.embeddings.create(model="text-embedding-3-small", input=[chunk])
            embedding = resp.data[0].embedding
            doc = {
                "text": chunk,
                "embedding": embedding,
                "file": os.path.basename(file_path),
                "chunk_id": i,
                "created_at": datetime.utcnow(),
                "metadata": {}
            }
            docs.append(doc)
    if not docs:
        return 0
    await db[collection_name].insert_many(docs)
    return len(docs)

async def vector_search_mongodb(query: str, collection_name: str = "rag_chunks", k: int = 4):
    """
    Perform a vector search in MongoDB Atlas for the most similar chunks to the query.
    """
    import openai
    import os
    openai.api_key = os.getenv("OPENAI_API_KEY")
    # Get embedding for the query
    resp = openai.embeddings.create(model="text-embedding-3-small", input=[query])
    query_embedding = resp.data[0].embedding
    
    pipeline = [
        {
            "$vectorSearch": {
                "queryVector": query_embedding,
                "path": "embedding",
                "numCandidates": 100,
                "limit": k,
                "index": "index"  # Use the correct Atlas vector index name
            }
        },
        {"$project": {"text": 1, "file": 1, "chunk_id": 1, "score": {"$meta": "vectorSearchScore"}}}
    ]
    results = []
    if db is None:
        raise RuntimeError("MongoDB connection is not initialized. Check your MONGO_URI.")
    async for doc in db[collection_name].aggregate(pipeline):
        results.append(doc)
    return results

class RAGService:
    def __init__(self):
        self.openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    async def search_properties(self, query: str, limit: int = 5) -> list:
        # Remove mock data. Use vector_search_mongodb for real retrieval.
        results = await vector_search_mongodb(query, k=limit)
        return results

    async def get_property_details(self, property_id: str) -> dict:
        """
        Retrieve property details from MongoDB by _id or chunk_id.
        """
        if db is None:
            raise RuntimeError("MongoDB connection is not initialized. Check your MONGO_URI.")
        from bson import ObjectId
        # Try to find by _id (ObjectId)
        try:
            doc = await db["rag_chunks"].find_one({"_id": ObjectId(property_id)})
            if doc:
                return doc
        except Exception:
            pass
        # Try to find by chunk_id (as string or int)
        doc = await db["rag_chunks"].find_one({"chunk_id": property_id})
        if doc:
            return doc
        try:
            doc = await db["rag_chunks"].find_one({"chunk_id": int(property_id)})
            if doc:
                return doc
        except Exception:
            pass
        return None

    async def generate_property_response(self, query: str, properties: list) -> str:
        """
        Use OpenAI LLM to generate a summary response for the given properties.
        """
        if not properties:
            return "Sorry, I couldn't find any properties matching your request. Please try a different search or provide more details."
        # Compose a prompt for the LLM
        property_texts = []
        for p in properties:
            if isinstance(p, dict):
                summary = p.get('text') or p.get('summary') or str(p)
                property_texts.append(f"- {summary}")
            else:
                property_texts.append(str(p))
        prompt = (
            f"You are a helpful real estate assistant. A user searched for: '{query}'. "
            f"Here are the top matching property listings from the database:\n\n"
            f"\n".join(property_texts) +
            "\n\nPlease summarize these properties for the user in a friendly, concise way."
        )
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Found {len(properties)} properties, but could not generate a summary: {e}" 