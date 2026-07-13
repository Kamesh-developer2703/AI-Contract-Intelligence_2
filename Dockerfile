# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
# - PYTHONUNBUFFERED: Prevents Python from buffering stdout/stderr (useful for real-time Docker logging)
# - PYTHONDONTWRITEBYTECODE: Prevents Python from writing .pyc files to disk
# - PIP_NO_CACHE_DIR: Disables pip caching to keep image size small
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=8000

# Set working directory inside the container
WORKDIR /app

# Install system dependencies
# - build-essential: Required for compilation of any C-extension packages
# - tesseract-ocr: Required by pytesseract for scanned PDF fallback OCR extraction
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements.txt first to maximize Docker build layer caching
COPY requirements.txt .

# Upgrade pip and install all Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Download spaCy pre-trained model for Named Entity Recognition (NER)
RUN python -m spacy download en_core_web_sm

# Copy the remaining project files into the container
COPY . .

# Expose the port FastAPI runs on
EXPOSE 8000

# Run the FastAPI server in production mode
# Binds to 0.0.0.0 to handle incoming traffic outside the container
CMD ["sh", "-c", "uvicorn api.main:app --host 0.0.0.0 --port ${PORT}"]
