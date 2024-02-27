FROM python:3.10.12-slim

# Set working directory
WORKDIR /workspace

# Install build tools and compilers
RUN apt-get update && apt-get install -y \
    ffmpeg \
    tesseract-ocr

# # Set CMAKE_ARGS environment variable
# ENV CMAKE_ARGS="-DLLAMA_CUBLAS=on"

# Install Requirements
RUN pip install -U \
    pip \
    setuptools \
    wheel

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY developer_requirements.txt .
RUN pip install -r developer_requirements.txt
