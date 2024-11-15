# Dockerfile for Knight's Shortest Path Finder (Streamlit App)
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

# Expose the port that Streamlit will run on
EXPOSE 8501

# Set environment variable to prevent Streamlit from launching a browser
ENV STREAMLIT_HEADLESS=true

# Command to run the Streamlit app
CMD ["streamlit", "run", "knight_paths.py", "--server.port=8501", "--server.address=0.0.0.0"]
