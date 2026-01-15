import sys
import os

# Add the backend directory to sys.path
sys.path.append(os.path.join(os.getcwd(), 'evolution-of-todo', 'backend'))

# Apply patches early
from app import patching

from sqlmodel import Session, select, create_engine
from app.models.user import User
from app.config import DATABASE_URL

# Fix DATABASE_URL if it's relative
if DATABASE_URL.startswith("sqlite:///./"):
    db_path = os.path.join(os.getcwd(), 'evolution-of-todo', 'backend', DATABASE_URL[12:])
    engine_url = f"sqlite:///{db_path}"
else:
    engine_url = DATABASE_URL

print(f"Connecting to DB at: {engine_url}")
engine = create_engine(engine_url)

def list_users():
    try:
        with Session(engine) as session:
            statement = select(User)
            users = session.exec(statement).all()
            print(f"Total users in DB: {len(users)}")
            for user in users:
                print(f"ID: {user.id}, Email: {user.email}")
    except Exception as e:
        print(f"Error listing users: {e}")

if __name__ == "__main__":
    list_users()
