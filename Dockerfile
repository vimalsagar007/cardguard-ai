FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (including curl and build tools)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy python dependencies spec
COPY pyproject.toml .
COPY README.md .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir .

# Copy application source code
COPY app/ ./app/
COPY data/ ./data/
COPY docs/ ./docs/
COPY frontend/ ./frontend/

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

EXPOSE 8080

CMD ["sh", "-c", "uvicorn app.api.main:app --host 0.0.0.0 --port ${PORT:-8080}"]
