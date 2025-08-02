from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models import conversation, message, user
from app.core.database import Base, engine
from app.api import crm, files, chat
from app.api.analytics import router as analytics_router
from app.api.advanced_features import router as advanced_router
from app.api.mongo_chat import router as mongo_chat_router

app = FastAPI(title="Multi-Agent Chat API")

# Enable CORS for all origins (for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or restrict to ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

@app.get("/health")
async def health():
    return {"status": "ok"}

app.include_router(crm.router)
app.include_router(files.router)
app.include_router(chat.router)
app.include_router(analytics_router)
app.include_router(advanced_router)
app.include_router(mongo_chat_router)
