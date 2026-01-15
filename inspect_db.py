import sqlite3
import os

db_path = os.path.join(os.getcwd(), 'evolution-of-todo', 'backend', 'todo.db')
print(f"Inspecting DB at: {db_path}")

if not os.path.exists(db_path):
    print("Database file does not exist!")
else:
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [t[0] for t in cursor.fetchall()]
        print(f"Tables: {tables}")
        
        user_table = None
        for t in tables:
            if t.lower() in ['user', 'users']:
                user_table = t
                break
        
        if user_table:
            cursor.execute(f"SELECT id, email FROM {user_table}")
            rows = cursor.fetchall()
            print(f"Users in '{user_table}' table: {len(rows)}")
            for row in rows:
                print(row)
        else:
            print("User table not found!")
        conn.close()
    except Exception as e:
        print(f"Error: {e}")
