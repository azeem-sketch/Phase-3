# AI-Generated Dockerfile for FastAPI Backend
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
# gcc and libpq-dev might be needed for some python packages, usually safest to include
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Expose port
EXPOSE 8000

# Start server using uvicorn directly for production
# Host 0.0.0.0 is crucial for Docker networking
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
