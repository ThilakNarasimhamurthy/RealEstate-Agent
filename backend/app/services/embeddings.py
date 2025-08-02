# app/services/embeddings.py
"""
DEPRECATED: This file contains legacy/test code for a simple vector database (SimpleVectorDB) with mock data.
Do NOT use in production. All property search and retrieval should use MongoDB Atlas vector search.
"""

import os
import json
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)

# --- DEPRECATED: SimpleVectorDB and related code ---
# class SimpleVectorDB:
#     """Simple vector database implementation for testing."""
#     ... (rest of class code commented out)

# # Global instance
# vector_db = SimpleVectorDB()

# def get_vector_db() -> SimpleVectorDB:
#     """Get the global vector database instance."""
#     return vector_db

def get_vector_db():
    """DEPRECATED: This function should not be used. Use MongoDB Atlas vector search instead."""
    raise NotImplementedError("SimpleVectorDB is deprecated. Use MongoDB Atlas vector search for all property retrieval.") 