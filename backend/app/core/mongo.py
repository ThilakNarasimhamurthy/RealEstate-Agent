# backend/app/core/mongo.py

from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "real_estate_ai")

print("[DEBUG] MONGO_URI:", MONGO_URI)

# Configure MongoDB client with SSL settings
if MONGO_URI:
    # Add SSL configuration to handle certificate issues
    if "mongodb+srv://" in MONGO_URI:
        # For MongoDB Atlas, add SSL configuration
        client = AsyncIOMotorClient(
            MONGO_URI,
            tls=True,
            tlsAllowInvalidCertificates=True,  # Only for development
            serverSelectionTimeoutMS=5000
        )
    else:
        client = AsyncIOMotorClient(MONGO_URI)
    
    db = client[MONGO_DB_NAME]
else:
    print("[WARNING] MONGO_URI not found in environment variables")
    client = None
    db = None