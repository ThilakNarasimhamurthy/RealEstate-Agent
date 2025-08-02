# app/models/message.py
import enum
from sqlalchemy import Column, Integer, Text, Enum, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Role(str, enum.Enum):
    user = "user"
    assistant = "assistant"

class Message(Base):
    __tablename__ = "messages"

    id              = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    role            = Column(Enum(Role), nullable=False)
    content         = Column(Text, nullable=False)
    created_at      = Column(DateTime(timezone=True), server_default=func.now())

    conversation    = relationship("Conversation", back_populates="messages")

    def __repr__(self) -> str:
        return f"<Message id={self.id} role={self.role}>"
