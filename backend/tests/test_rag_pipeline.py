import asyncio
from app.services.rag_service import ingest_document_to_mongodb, vector_search_mongodb

async def main():
    # 1. Ingest the hackathon knowledge base CSV (correct file path)
    num_chunks = await ingest_document_to_mongodb("backend/HackathonInternalKnowledgeBase.csv")
    print(f"Ingested {num_chunks} chunks.")

    # 2. Run a vector search query
    query = "What is the hackathon submission deadline?"
    results = await vector_search_mongodb(query)
    print(f"Top results for query: '{query}'")
    for i, doc in enumerate(results):
        print(f"\nResult {i+1}:")
        print("Text:", doc.get("text"))
        print("Score:", doc.get("score", "N/A"))
        print("Metadata:", doc.get("metadata", {}))

if __name__ == "__main__":
    asyncio.run(main()) 