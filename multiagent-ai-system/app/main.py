from fastapi import FastAPI
from app.models import conversation, message, user
from app.core.database import Base, engine
from app.api import crm, files, chat 
app = FastAPI()
Base.metadata.create_all(bind=engine)

@app.get("/health")
async def health():
    return {"status": "ok"}


app = FastAPI(title="Multi-Agent Chat API")

app.include_router(crm.router)
app.include_router(files.router)
app.include_router(chat.router)
