"""User data model."""
from __future__ import annotations
from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy.orm import relationship

class User(SQLModel, table=True):
    """User model for authentication and ownership."""
    __tablename__ = "users"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    password_hash: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationship to todos - using explicit SQLAlchemy relationship for Python 3.14 compatibility
    todos: List["Todo"] = Relationship(
        sa_relationship=relationship("Todo", back_populates="user", cascade="all, delete-orphan")
    )
