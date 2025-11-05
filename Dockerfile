# Base image with Python; slim to reduce image size
FROM python:3.11-slim

# Prevent Python from buffering stdout/stderr and writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    # Reduce TF log verbosity (0=all, 1=info, 2=warning, 3=error)
    TF_CPP_MIN_LOG_LEVEL=2

# Set work directory
WORKDIR /app

# Install system dependencies needed by scientific Python/TensorFlow
# and image processing libs
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies first for better build caching
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py ./
COPY templates ./templates
COPY static ./static
COPY model ./model

# Expose the Flask/gunicorn port
EXPOSE 5000

# Use gunicorn for a production-ready server
# app:app matches the Flask instance variable in app.py
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "app:app"]