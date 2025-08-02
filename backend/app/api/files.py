from fastapi import APIRouter, UploadFile, File, HTTPException, status
from pathlib import Path
import uuid, shutil, mimetypes, time

from ..services.rag_service import ingest_document_to_mongodb
import uuid, shutil, mimetypes, time

router = APIRouter(tags=["files"])

UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/upload_docs", status_code=status.HTTP_201_CREATED)
async def upload_docs(file: UploadFile = File(...)):
    """
    Upload and ingest a document into the MongoDB vector database.
    Supports .txt, .csv files for now.
    """
    if not file.filename:
        raise HTTPException(400, "No filename provided")
    
    ext = Path(file.filename).suffix.lower()
    if ext not in {".csv", ".txt"}:
        raise HTTPException(400, "unsupported file type. Currently supports .txt and .csv files.")
    
    # Save uploaded file
    dest = UPLOAD_DIR / f"{uuid.uuid4()}{ext}"
    with dest.open("wb") as out:
        shutil.copyfileobj(file.file, out)

    # Ingest into MongoDB vector database
    try:
        chunks_ingested = await ingest_document_to_mongodb(str(dest))
        
        meta = {
            "saved_as": str(dest),
            "orig_name": file.filename,
            "mime": mimetypes.guess_type(dest)[0],
            "size_bytes": dest.stat().st_size,
            "uploaded_at": int(time.time()),
            "chunks_ingested": chunks_ingested,
            "status": "success"
        }
        return meta
    except Exception as e:
        # Clean up file if ingestion fails
        if dest.exists():
            dest.unlink()
        raise HTTPException(500, f"Failed to ingest document: {str(e)}")

@router.get("/ingest_status")
async def get_ingest_status():
    """
    Get status of document ingestion and vector database.
    """
    from ..core.mongo import db
    if db is None:
        raise HTTPException(500, "MongoDB connection not available")
    
    try:
        # Count documents in rag_chunks collection
        total_chunks = await db.rag_chunks.count_documents({})  # type: ignore[attr-defined]
        
        # Get unique files
        pipeline = [
            {"$group": {"_id": "$file", "chunks": {"$sum": 1}}}
        ]
        files = await db.rag_chunks.aggregate(pipeline).to_list(None)  # type: ignore[attr-defined]
        
        return {
            "total_chunks": total_chunks,
            "unique_files": len(files),
            "files": [{"filename": f["_id"], "chunks": f["chunks"]} for f in files]
        }
    except Exception as e:
        raise HTTPException(500, f"Failed to get ingestion status: {str(e)}")
