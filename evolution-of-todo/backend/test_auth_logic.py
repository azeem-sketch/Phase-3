import os
import sys

# Standard patching for 3.14 if needed
import typing
if hasattr(typing, '_eval_type'):
    original_eval_type = typing._eval_type
    def patched_eval_type(*args, **kwargs):
        kwargs.pop('prefer_fwd_module', None)
        kwargs.pop('type_params', None)
        return original_eval_type(*args, **kwargs)
    typing._eval_type = patched_eval_type

sys.path.append(os.getcwd())

from app.core.auth import hash_password, verify_password
from app.api.auth import signup, signin
from app.schemas.auth import UserSignup, UserSignin
from app.database import get_session
from sqlmodel import Session, create_engine, SQLModel

def test_auth():
    email = "longpwd@test.com"
    password = "a" * 200 # VERY LONG PASSWORD
    
    print(f"Testing signup for {email}...")
    
    # Use the same engine as the app
    from app.database import engine
    
    with Session(engine) as session:
        # 1. Test hash/verify directly
        hp = hash_password(password)
        print(f"Hash: {hp}")
        if verify_password(password, hp):
            print("Direct hash verification: PASS")
        else:
            print("Direct hash verification: FAIL")
            return

        # 2. Test Signup logic
        try:
            # Clean up old test user if exists
            from app.models.user import User
            from sqlmodel import select
            existing = session.exec(select(User).where(User.email == email)).first()
            if existing:
                session.delete(existing)
                session.commit()
                print("Cleaned up existing user.")
            
            # Signup
            data = UserSignup(email=email, password=password)
            # We call the endpoint logic directly (need to pass session)
            from app.api.auth import signup
            res = signup(data, session)
            print(f"Signup logic: PASS (Created user ID: {res.id})")
        except Exception as e:
            print(f"Signup logic: FAIL ({e})")
            return

        # 3. Test Signin logic
        try:
            creds = UserSignin(email=email, password=password)
            from app.api.auth import signin
            token_res = signin(creds, session)
            print(f"Signin logic: PASS (Token: {token_res.access_token[:20]}...)")
        except Exception as e:
            print(f"Signin logic: FAIL ({e})")
            return

if __name__ == "__main__":
    test_auth()
