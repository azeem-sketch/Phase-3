import sqlite3
import os
from passlib.hash import pbkdf2_sha256

db_path = r'C:\Users\azeem\OneDrive\Desktop\evolution of to doapp\evolution-of-todo\backend\todo.db'

def final_db_check():
    if not os.path.exists(db_path):
        print(f"❌ DB NOT FOUND AT: {db_path}")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id, email, password_hash FROM users")
    rows = cursor.fetchall()
    
    print(f"Found {len(rows)} users:")
    for row in rows:
        uid, email, phash = row
        match = pbkdf2_sha256.verify("password123", phash)
        print(f"ID: {uid} | Email: '{email}' | Raw Email Type: {type(email)} | Match 'password123': {match}")
    
    conn.close()

if __name__ == "__main__":
    final_db_check()
