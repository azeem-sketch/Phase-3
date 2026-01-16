"""FastAPI application entry point."""
from . import patching

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import time
from app.config import CORS_ORIGINS
from app.database import init_db
from app.api import auth, todos
print(f"DEBUG: CORS_ORIGINS configured as: {CORS_ORIGINS}")

app = FastAPI(
    title="Evolution of Todo API",
    description="Phase II: Full-Stack Web Application",
    version="2.0.0"
)

# Configure CORS
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f"DEBUG: {request.method} {request.url.path} - {response.status_code} ({process_time:.4f}s)")
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:3000", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth.router)
app.include_router(tasks.router)

@app.on_event("startup")
def on_startup():
    """Initialize database on startup."""
    print("DEBUG: Application starting up and initializing DB")
    init_db()

@app.get("/")
def root():
    """Root endpoint."""
    print("DEBUG: Root endpoint hit")
    return {"message": "Evolution of Todo API - Phase II", "status": "running"}

@app.get("/health")
def health():
    """Health check endpoint."""
    print("DEBUG: Health check endpoint hit")
    return {"status": "healthy"}
