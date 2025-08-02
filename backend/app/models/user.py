# app/models/user.py
from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship           
from app.core.database import Base


class User(Base):
    __tablename__ = "users"                      # DB table name

    id         = Column(Integer, primary_key=True, index=True)
    email      = Column(String, unique=True, index=True, nullable=False)
    name       = Column(String, nullable=True)
    company    = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self) -> str:                   # handy for debugging
        return f"<User id={self.id} email={self.email!r}>"
    
    conversations = relationship("Conversation", back_populates="user")
