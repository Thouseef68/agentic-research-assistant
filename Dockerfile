# Use an official lightweight Python runtime
FROM python:3.10-slim

# Set system work environments
WORKDIR /app

# 💡 FIXED: Removed software-properties-common to prevent minimal Debian repo search crashes
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the complete codebase into the container runtime space
COPY . .

# Expose the standard web communications gateway port
EXPOSE 8000

# Fire up the production high-concurrency Uvicorn engine
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]