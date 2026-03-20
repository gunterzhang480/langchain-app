FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies (needed for some AI libraries)
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your code
COPY . .

# Run the FastAPI app on port 8080 (Cloud Run's default)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]