# Base Python image
FROM python:3.10-slim

# Install system packages for Tesseract, PDF, and image handling
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    poppler-utils \
    libgl1 \
    curl \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Install Cloudflare Tunnel CLI
RUN curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 \
    -o /usr/local/bin/cloudflared && chmod +x /usr/local/bin/cloudflared

# Set working directory
WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files
COPY . .

# Expose FastAPI default port
EXPOSE 8000

# Command to start both FastAPI and Cloudflare Tunnel
CMD uvicorn main:app --host 0.0.0.0 --port 8000 & \
    cloudflared tunnel --url http://localhost:8000
