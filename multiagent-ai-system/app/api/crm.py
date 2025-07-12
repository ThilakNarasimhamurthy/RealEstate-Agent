from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db                       # session dependency
from app.services.crm import (                             # ← helpers live here now
    create_user, get_user_by_email, get_user,
    create_conversation, get_messages,
)

from app.schemas import user as user_s
from typing import List

router = APIRouter(prefix="/crm", tags=["crm"])

# POST /crm/create_user
@router.post("/create_user", response_model=user_s.UserOut,
             status_code=status.HTTP_201_CREATED)
def create_user_ep(payload: user_s.UserCreate, db: Session = Depends(get_db)):
    if get_user_by_email(db, payload.email):
        raise HTTPException(400, "email already exists")
    return create_user(db, email=payload.email, name=payload.name,
                       company=payload.company)

# PUT /crm/update_user
@router.put("/update_user/{user_id}", response_model=user_s.UserOut)
def update_user_ep(user_id: int, payload: user_s.UserUpdate,
                   db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(404, "user not found")
    if payload.name is not None:
        user.name = payload.name
    if payload.company is not None:
        user.company = payload.company
    db.commit(); db.refresh(user)
    return user

# GET /crm/conversations/{user_id}   (stub = list IDs only)
@router.get("/conversations/{user_id}", response_model=List[int])
def list_conversations_ep(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(404, "user not found")
    return [c.id for c in user.conversations]
