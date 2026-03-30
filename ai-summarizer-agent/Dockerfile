FROM python:3.10-slim

WORKDIR /app

# Improve runtime behavior in containers
ENV PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Cloud Run requires the service to listen on PORT 8080
ENV PORT=8080

# Run the application
CMD ["python", "main.py"]
