"""Database models for user module."""

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from postagram.db.database import Base


class User(Base):
    """User model."""

    __tablename__ = "users"

    id = Column(String(36), primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
    posts = relationship("Post", back_populates="user")
