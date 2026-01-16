"""API dependencies."""
from typing import Annotated
from fastapi import Depends, Header
from sqlmodel import Session, select
from app.database import get_session
from app.models.user import User
from app.core.auth import decode_access_token
from app.core.exceptions import AuthenticationError

def get_current_user(
    authorization: Annotated[str | None, Header()] = None,
    session: Session = Depends(get_session)
) -> User:
    """Dependency to get the current authenticated user."""
    if not authorization:
        raise AuthenticationError("Missing authorization header")
    
    # Extract token from "Bearer <token>"
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise AuthenticationError("Invalid authorization header format")
    
    token = parts[1]
    
    # Decode token
    payload = decode_access_token(token)
    if not payload:
        raise AuthenticationError("Invalid or expired token")
    
    # Get user ID from payload (Better Auth usually uses 'sub')
    user_id = payload.get("sub") or payload.get("id")
    if not user_id:
        raise AuthenticationError("Invalid token payload: missing user ID")
    
    # Query user from database
    # Handle the fact that user_id from JWT might be a string (e.g. from Better Auth)
    if isinstance(user_id, str) and user_id.isdigit():
        user_id = int(user_id)
        
    statement = select(User).where(User.id == user_id)
    user = session.exec(statement).first()
    
    # If user doesn't exist in our DB but authenticated via Better Auth, 
    # we might need to "jit" create them or just error.
    # The spec implies users exist in Neon DB first.
    if not user:
         # Try looking up by email if available in payload
         email = payload.get("email")
         if email:
             user = session.exec(select(User).where(User.email == email)).first()
    
    if not user:
        raise AuthenticationError("User not found in system")
    
    return user
