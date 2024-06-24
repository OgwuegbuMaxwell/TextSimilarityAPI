# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Install system dependencies required for PyPI packages that need compilation
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    libffi-dev \
    python3-dev \
    libssl-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies with an increased timeout
RUN pip install --default-timeout=1200 --no-cache-dir -r requirements.txt

# Copy the spaCy model tar.gz file
COPY en_core_web_md-3.7.1.tar.gz .

# Install the spaCy model
RUN pip install --default-timeout=1200 en_core_web_md-3.7.1.tar.gz

# Copy the rest of the application
COPY . .

CMD ["python", "app.py"]
