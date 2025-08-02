from app.core.mongo import db
import asyncio

async def drop_rag_chunks():
    if db is None:
        print("[ERROR] MongoDB connection is not initialized. Check your MONGO_URI.")
        return
    await db["rag_chunks"].drop()
    print("rag_chunks collection dropped.")

if __name__ == "__main__":
    asyncio.run(drop_rag_chunks()) 