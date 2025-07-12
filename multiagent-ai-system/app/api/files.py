from fastapi import APIRouter, UploadFile, File, HTTPException, status
from pathlib import Path
from app.services.embeddings import ingest_file   
import uuid, shutil, mimetypes, time

router = APIRouter(tags=["files"])

UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/upload_docs", status_code=status.HTTP_201_CREATED)
async def upload_docs(file: UploadFile = File(...)):
    ext = Path(file.filename).suffix.lower()
    if ext not in {".pdf", ".csv", ".txt"}:
        raise HTTPException(400, "unsupported file type")
    dest = UPLOAD_DIR / f"{uuid.uuid4()}{ext}"
    with dest.open("wb") as out:
        shutil.copyfileobj(file.file, out)

    meta = {
        "saved_as": str(dest),
        "orig_name": file.filename,
        "mime": mimetypes.guess_type(dest)[0],
        "size_bytes": dest.stat().st_size,
        "uploaded_at": int(time.time())
    }
    ingest_file(dest)   
    return meta          # later you’ll insert meta into a table
