# app/api/chat.py
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from utils.llm import chat as llm_chat
from app.services.embeddings import search
from app.services.history import last_messages
from pathlib import Path

from app.services.crm import (
    get_user, create_conversation, get_conversation,
    add_message, Role
)
from app.core.database import get_db
SYSTEM_PROMPT = Path("config/prompt.txt").read_text()
router = APIRouter(tags=["chat"])

class ChatReq(BaseModel):
    user_id: int
    message: str

class ChatResp(BaseModel):
    reply: str

MAX_HISTORY = 6     # last N turns to include
K_SNIPPETS  = 3     # top-k RAG results

@router.post("/chat", response_model=ChatResp)
def chat(req: ChatReq, db: Session = Depends(get_db)):
    # 1. ensure user exists (stub-simple)
    user = get_user(db, req.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")

    # 2. fetch or create an active conversation
    conv = user.conversations[-1] if user.conversations else None
    if conv is None:
        conv = create_conversation(db, user_id=user.id)

    # 3. save *user* message to DB immediately
    user_msg = add_message(db, conv_id=conv.id, role=Role.user, content=req.message)

    # 4. pull history + RAG snippets
    history = last_messages(db, conv.id, MAX_HISTORY)
    snippets = search(req.message, k=K_SNIPPETS)

    # 5. craft OpenAI messages list
    messages = [
             {"role": "system", "content": SYSTEM_PROMPT}
    ]

    for m in history:
        messages.append({"role": m.role.value, "content": m.content})

    if snippets:
        joined = "\n---\n".join(snippets)
        messages.append({"role": "system", "content": f"Context snippets:\n{joined}"})

    messages.append({"role": "user", "content": req.message})

    # 6. call GPT with retry/timeout
    assistant_reply = llm_chat(messages)

    # 7. store assistant reply
    add_message(db, conv_id=conv.id, role=Role.assistant, content=assistant_reply)

    return {"reply": assistant_reply}
