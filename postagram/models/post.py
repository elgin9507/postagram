"""Database models for post module."""

from sqlalchemy import Column, ForeignKey, String, Text
from sqlalchemy.orm import relationship

from postagram.db.database import Base


class Post(Base):
    """Post model."""

    __tablename__ = "posts"

    id = Column(String(36), primary_key=True, index=True)
    user_id = Column(String(36), ForeignKey("users.id"))
    user = relationship("User", back_populates="posts")
    text = Column(Text)
