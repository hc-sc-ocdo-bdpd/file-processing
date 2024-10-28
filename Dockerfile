FROM python:3.10.12-slim

# Set working directory
WORKDIR /workspace

# Install system dependencies if needed
RUN apt-get update && apt-get install -y \
    ffmpeg \
    tesseract-ocr

# Upgrade pip, setuptools, and wheel
RUN pip install -U \
    pip \
    setuptools \
    wheel

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt
