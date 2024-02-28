FROM python:3.10.12-slim

# Set working directory
WORKDIR /workspace

RUN apt-get update && apt-get install -y \
    ffmpeg \
    tesseract-ocr

RUN pip install -U \
    pip \
    setuptools \
    wheel

COPY requirements.txt .
COPY developer_requirements.txt .
RUN pip install -r requirements.txt

# docker build --build-arg DEV=true -t file_processing_tools:latest .
# Whether to install optional dependencies
ARG DEV=false

RUN if [ "${DEV}" = "true" ]; then \
      pip install -r developer_requirements.txt; \
    fi
