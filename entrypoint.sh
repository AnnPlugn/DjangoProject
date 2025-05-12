#!/bin/bash

# Wait for the database to be ready
echo "Waiting for PostgreSQL..."

while ! nc -z db 5432; do
  sleep 0.1
done

echo "PostgreSQL started"

# Run migrations
echo "Running migrations..."
python manage.py migrate

# Start the Django development server
echo "Starting Django development server..."
exec python manage.py runserver 0.0.0.0:8000