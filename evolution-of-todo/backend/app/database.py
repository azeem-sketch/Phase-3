"""Database configuration and session management."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.config import DATABASE_URL

# Create database engine
connect_args = {"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
engine = create_engine(DATABASE_URL, echo=True, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_session():
    """Dependency to get database session."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

def init_db():
    """Initialize database tables."""
    # We delay the SQLModel import here to avoid global hang
    try:
        from sqlmodel import SQLModel
        from app.models import user, todo, task, chat # Import models to register them
        SQLModel.metadata.create_all(engine)
        print("DEBUG: init_db completed successfully")
    except Exception as e:
        print(f"DEBUG: Error in init_db (likely SQLModel hang): {e}")

# Define a dummy SQLModel if needed by other files importing from here
# Actually, better to just let them import it and see if they hang later.
