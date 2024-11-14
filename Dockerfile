# Dockerfile for Knight's Shortest Path Finder
FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        graphviz \
        libfreetype6-dev \
        libpng-dev \
        libjpeg-dev \
        zlib1g-dev \
        fonts-dejavu-core \
        build-essential \
        && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set default command
CMD ["python", "knight_paths.py"]
