FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libc-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies with compatible versions
RUN pip install --no-cache-dir --upgrade pip
# Install compatible MongoDB drivers first
RUN pip install --no-cache-dir motor==3.5.1 pymongo==4.8.0
# Install the rest of the requirements
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Set environment variables for production
ENV PYTHONUNBUFFERED=1
ENV PYTHONOPTIMIZE=1

# Create non-root user for security
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port (Koyeb will set PORT env var)
EXPOSE 8080

CMD ["python", "-m", "FileStream"]