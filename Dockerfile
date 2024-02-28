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
COPY dist/file_processing-0.0.0-py3-none-any.whl .

# docker build --build-arg DEV=true -t file_processing_tools:latest .
# Whether to install optional dependencies
ARG DEV=false

RUN if [ "${DEV}" = "true" ]; then \
        pip install -r developer_requirements.txt; && \
        pip install -r requirements.txt; \
    else \
        pip install file_processing-0.0.0-py3-none-any.whl; \
    fi
