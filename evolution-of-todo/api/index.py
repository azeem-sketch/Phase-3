import sys
import os

# Add the backend directory to sys.path so we can import from app
# backend is at ../backend relative to api/index.py
sys.path.append(os.path.join(os.path.dirname(__file__), '../backend'))

from app.main import app
