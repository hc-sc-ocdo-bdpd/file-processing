FROM python:3.10.4-slim

# Set working directory
WORKDIR /workspace

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    tesseract-ocr \
    git

# Upgrade pip, setuptools, and wheel
RUN pip install -U \
    pip \
    setuptools \
    wheel

# Copy the requirements file and install dependencies
COPY requirements.txt requirements-dev.txt ./
RUN pip install -r requirements.txt -r requirements-dev.txt

# Copy the entire project directory into the container
COPY . .