
# Python Image 
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# SYSTEM DEPENDENCIES
# Install essential packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# PYTHON DEPENDENCIES
# Copy dependency file
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy Application Files
COPY . .

# PRISMA SETUP
# Install Prisma CLI and generate client
RUN pip install prisma && prisma generate

# EXPOSE PORT
EXPOSE 8000

# Default command to start FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
