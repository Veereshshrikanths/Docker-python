# Use an official Python slim image
FROM python:3.11-slim

# Set working dir
WORKDIR /app

# Install system dependencies needed for psycopg2 (small)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
 && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app
COPY app.py .

# Make script executable (optional)
RUN chmod +x /app/app.py

# Default environment variables (can be overridden when running)
ENV DB_HOST=postgres \
    DB_PORT=5432 \
    DB_NAME=testdb \
    DB_USER=testuser \
    DB_PASSWORD=testpass

# Run the app
CMD ["python", "app.py"]
