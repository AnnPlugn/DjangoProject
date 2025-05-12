# Use the official Python runtime image
FROM python:3.11-slim

# Set environment variables to prevent __pycache__/ files and unbuffered output
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Create and set the working directory
WORKDIR /app

# Upgrade pip
RUN pip install --upgrade pip

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install netcat and postgresql-client for psql
RUN apt-get update && apt-get install -y netcat-openbsd postgresql-client && rm -rf /var/lib/apt/lists/*

# Copy the rest of the application code
COPY . .

# Copy and make the entrypoint script executable
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

# Expose the Django port
EXPOSE 8000

# Set the entrypoint
ENTRYPOINT ["./entrypoint.sh"]

# Default command (overridden by docker-compose)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]