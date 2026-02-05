"""Todo data model."""
from __future__ import annotations
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy.orm import relationship, Mapped

class Todo(SQLModel, table=True):
    """Todo model for task management."""
    __tablename__ = "todos"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationship to user (Commented out for 3.14 compat)
    # user: Mapped["User"] = Relationship(back_populates="todos")
