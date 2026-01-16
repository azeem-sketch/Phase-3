"""Database configuration and session management."""
from sqlmodel import create_engine, Session, SQLModel
from app.config import DATABASE_URL

# Create database engine
connect_args = {"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
engine = create_engine(DATABASE_URL, echo=True, connect_args=connect_args)

def get_session():
    """Dependency to get database session."""
    with Session(engine) as session:
        yield session

def init_db():
    """Initialize database tables."""
    SQLModel.metadata.create_all(engine)
