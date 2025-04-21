# Use official Python slim image as base
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=app.py \
    FLASK_ENV=production

# Create a non-root user for security
RUN adduser --disabled-password --gecos '' appuser

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create templates directory
RUN mkdir -p /app/templates

# Copy the application code and templates
COPY ./src/service-a/app.py /app/
COPY ./src/service-a/templates/* /app/templates/

# Change ownership of the app directory to appuser
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 5000 9090

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
