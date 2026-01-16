"""Application configuration."""
import os
from dotenv import load_dotenv

load_dotenv()

# Database
DATABASE_URL = os.getenv("DATABASE_URL", "")

# Security
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
BETTER_AUTH_SECRET = os.getenv("BETTER_AUTH_SECRET", "a_very_secret_key_1234567890_abcdefghijklmnopqrstuvwxyz")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24

# CORS
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

# Environment
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
