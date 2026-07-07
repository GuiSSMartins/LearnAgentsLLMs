# ==========================================
# Base Image
# ==========================================
FROM python:3.12-sli

# Prevent Python from creating .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Show logs immediately
ENV PYTHONUNBUFFERED=1

# ==========================================
# Install system dependencies
# ==========================================
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# ==========================================
# Create working directory
# ==========================================
WORKDIR /app

# ==========================================
# Install Python dependencies
# ==========================================
COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

# ==========================================
# Copy project
# ==========================================
COPY app ./app

COPY data ./data

# Chroma database directory
RUN mkdir -p /app/chroma

# ==========================================
# Expose FastAPI port
# ==========================================
EXPOSE 8000

# ==========================================
# Start FastAPI
# ==========================================
CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]