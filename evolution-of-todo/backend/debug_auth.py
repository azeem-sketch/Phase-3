import sys
import os

# Add current directory to path to ensure app module is found
sys.path.append(os.getcwd())

from sqlmodel import Session, select
from app.database import engine
from app.models.user import User

def list_users():
    with Session(engine) as session:
        users = session.exec(select(User)).all()
        if not users:
            print("No users found in database.")
        else:
            print(f"Found {len(users)} users:")
            for user in users:
                print(f"ID: {user.id}, Email: {user.email}, Name: {user.full_name}")

if __name__ == "__main__":
    list_users()
