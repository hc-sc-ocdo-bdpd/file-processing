FROM python:3.10.12-slim

# Set working directory
WORKDIR /workspace

# docker build --build-arg DEV=true --build-arg FULL=true -t file_processing_tools:latest .
# Whether to install optional dependencies
ARG DEV=false
ARG FULL=false

RUN if [ "${FULL}" = "true" ]; then \
    apt-get update && apt-get install -y \
        ffmpeg \
        tesseract-ocr; \
    fi

RUN pip install -U \
    pip \
    setuptools \
    wheel

COPY dist/file_processing-0.0.0-py3-none-any.whl .

RUN if [ "${DEV}" = "true" ] && [ "${FULL}" = "true" ]; then \
        pip install file_processing-0.0.0-py3-none-any.whl[developer,full]; \
    elif [ "${DEV}" = "true" ]; then \
        pip install file_processing-0.0.0-py3-none-any.whl[developer]; \
    elif [ "${FULL}" = "true" ]; then \
        pip install file_processing-0.0.0-py3-none-any.whl[full]; \
    else \
        pip install file_processing-0.0.0-py3-none-any.whl; \
    fi
