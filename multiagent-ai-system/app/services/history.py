# app/services/history.py
from sqlalchemy.orm import Session
from app.models.message import Message
from typing import List

def last_messages(db: Session, conv_id: int, n: int = 6) -> List[Message]:
    """
    Return the most recent `n` messages for this conversation,
    newest-to-oldest order.
    """
    return (db.query(Message)
              .filter_by(conversation_id=conv_id)
              .order_by(Message.id.desc())
              .limit(n)
              .all()[::-1])     # reverse to oldest-first
