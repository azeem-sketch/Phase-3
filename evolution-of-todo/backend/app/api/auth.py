"""Authentication endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.database import get_session
from app.models.user import User
from app.schemas.auth import UserSignup, UserSignin, UserResponse, Token
from app.core.auth import hash_password, verify_password, create_access_token
from app.core.exceptions import ValidationError, AuthenticationError
from app.api.deps import get_current_user

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def signup(user_data: UserSignup, session: Session = Depends(get_session)):
    """Register a new user."""
    email = user_data.email.lower().strip()
    password = user_data.password.strip()
    print(f"DEBUG: Signup attempt for normalized email: {email}")
    # Check if email already exists
    statement = select(User).where(User.email == email)
    existing_user = session.exec(statement).first()
    
    if existing_user:
        raise ValidationError("Email already in use")
    
    # Hash password
    password_hash = hash_password(user_data.password)
    
    # Create user
    user = User(
        email=email,
        password_hash=password_hash
    )
    
    session.add(user)
    session.commit()
    session.refresh(user)
    print(f"DEBUG: Successfully created user {user.id}")
    
    return user
@router.post("/signin", response_model=Token)
def signin(credentials: UserSignin, session: Session = Depends(get_session)):
    """Authenticate a user and return a token."""
    email = credentials.email.lower().strip()
    password = credentials.password.strip()
    print(f"DEBUG: Signin attempt for normalized email: {email}")
    # Query user by email
    statement = select(User).where(User.email == email)
    user = session.exec(statement).first()
    
    if not user:
        print(f"DEBUG: Signin failed - User not found: {email}")
        raise AuthenticationError("Invalid email or password")
    
    # Verify password
    if not verify_password(password, user.password_hash):
        print(f"DEBUG: Signin failed - Password mismatch for: {email}")
        raise AuthenticationError("Invalid email or password")
    
    print(f"DEBUG: Signin successful for {email}")
    
    # Create access token
    access_token = create_access_token({"sub": str(user.id)})
    
    return Token(
        access_token=access_token,
        user=UserResponse.model_validate(user)
    )

@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information."""
    return current_user
