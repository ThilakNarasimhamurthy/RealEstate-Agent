from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.user import User
from app.models.conversation import Conversation
from app.models.message import Message, Role

# ---------- USER ----------
def create_user(db: Session, *, email: str, name: str | None = None,
                company: str | None = None) -> User:
    user = User(email=email, name=name, company=company)
    db.add(user); db.commit(); db.refresh(user)
    return user

def get_user(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter_by(id=user_id).first()

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter_by(email=email).first()

# ---------- CONVERSATION ----------
def create_conversation(db: Session, *, user_id: int) -> Conversation:
    conv = Conversation(user_id=user_id)
    db.add(conv); db.commit(); db.refresh(conv)
    return conv

def get_conversation(db: Session, conv_id: int) -> Optional[Conversation]:
    return db.query(Conversation).filter_by(id=conv_id).first()

# ---------- MESSAGE ----------
def add_message(db: Session, *, conv_id: int, role: Role, content: str) -> Message:
    msg = Message(conversation_id=conv_id, role=role, content=content)
    db.add(msg); db.commit(); db.refresh(msg)
    return msg

def get_messages(db: Session, conv_id: int, limit: int | None = None) -> List[Message]:
    q = (db.query(Message)
           .filter_by(conversation_id=conv_id)
           .order_by(Message.id))
    if limit:
        q = q.limit(limit)
    return q.all()
