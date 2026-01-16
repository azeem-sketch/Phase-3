"""Authentication schemas."""
from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

class UserSignup(BaseModel):
    """Schema for user signup."""
    email: str
    password: str = Field(min_length=8, max_length=100)

class UserSignin(BaseModel):
    """Schema for user signin."""
    email: str
    password: str

class UserResponse(BaseModel):
    """Schema for user response."""
    id: int
    email: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    """Schema for authentication token."""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
