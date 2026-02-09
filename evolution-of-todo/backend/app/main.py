"""FastAPI application entry point."""
from . import patching

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import time
from app.config import CORS_ORIGINS
from app.database import init_db
from app.api import auth, tasks, chat
print(f"DEBUG: CORS_ORIGINS configured as: {CORS_ORIGINS}")

app = FastAPI(
    title="Evolution of Todo API",
    description="Phase II: Full-Stack Web Application",
    version="2.0.0"
)

# Outermost Middleware: CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers with consistent /api prefix
app.include_router(auth.router, prefix="/api")
app.include_router(tasks.router, prefix="/api")
app.include_router(chat.router, prefix="/api")

@app.on_event("startup")
def on_startup():
    """Initialize database on startup."""
    print("DEBUG: Application starting up and initializing DB")
    init_db()

@app.get("/")
def root():
    """Root endpoint."""
    print("DEBUG: Root endpoint hit - MARKER: 99999")
    return {"message": "Evolution of Todo API - Phase II", "status": "running", "marker": "99999"}

@app.get("/health")
def health():
    """Health check endpoint."""
    print("DEBUG: Health check endpoint hit")
    return {"status": "healthy"}
