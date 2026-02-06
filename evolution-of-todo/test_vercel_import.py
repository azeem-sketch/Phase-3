import sys
import os

# Simulate Vercel environment path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

try:
    print("Attempting to import app.main...")
    from app.main import app
    print("SUCCESS: app.main imported successfully.")
except Exception as e:
    print(f"FAILURE: {e}")
    import traceback
    traceback.print_exc()
