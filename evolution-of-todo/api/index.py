import sys
import os

# Add the backend directory to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '../backend'))

try:
    from app.main import app
except ImportError as e:
    # Fallback to a basic FastAPI app if import fails to prevent 500 error during discovery
    from fastapi import FastAPI
    app = FastAPI()
    @app.get("/api/error")
    def error():
        import traceback
        return {
            "error": str(e),
            "traceback": traceback.format_exc(),
            "path": sys.path,
            "cwd": os.getcwd()
        }
