# app/mcp/servers/crm_server.py
"""
CRM (Customer Relationship Management) server for MCP.
Moved from app/services/crm.py
"""

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


class CRMServer:
    """MCP CRM server for user and conversation management."""
    
    def __init__(self, db_session: Session):
        self.db = db_session
        self.name = "crm_server"
        
    def create_user(self, email: str, name: str | None = None, 
                   company: str | None = None) -> User:
        """Create a new user."""
        return create_user(self.db, email=email, name=name, company=company)
        
    def get_user(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        return get_user(self.db, user_id)
        
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        return get_user_by_email(self.db, email)
        
    def create_conversation(self, user_id: int) -> Conversation:
        """Create a new conversation for a user."""
        return create_conversation(self.db, user_id=user_id)
        
    def get_conversation(self, conv_id: int) -> Optional[Conversation]:
        """Get conversation by ID."""
        return get_conversation(self.db, conv_id)
        
    def add_message(self, conv_id: int, role: Role, content: str) -> Message:
        """Add a message to a conversation."""
        return add_message(self.db, conv_id=conv_id, role=role, content=content)
        
    def get_messages(self, conv_id: int, limit: int | None = None) -> List[Message]:
        """Get messages for a conversation."""
        return get_messages(self.db, conv_id, limit=limit) 