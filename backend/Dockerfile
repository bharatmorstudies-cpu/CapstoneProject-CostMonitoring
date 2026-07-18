# Use an explicit, lightweight optimized Python runtime image
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Install system dependencies needed for compiling package assets
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file first to maximize Docker layer caching speed
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source modules into the workspace
COPY ./app ./app

# Expose backend network container port
EXPOSE 8000

# Launch the FastAPI app server asynchronously via Uvicorn on startup
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
