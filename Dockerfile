# Use the Python 3.10.4 slim image
FROM python:3.10.4-slim

# Set working directory
WORKDIR /workspace

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    tesseract-ocr \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy requirements files and install dependencies
COPY requirements.txt requirements-dev.txt ./
RUN pip install --no-cache-dir -r requirements.txt -r requirements-dev.txt

# Copy all application files (necessary for GitHub Actions)
COPY . .