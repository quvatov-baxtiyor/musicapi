#!/bin/bash

# Wait for the database to be ready
echo "Waiting for the database..."
sleep 10

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start Gunicorn
echo "Starting Gunicorn..."
exec gunicorn --bind 0.0.0.0:8000 Netflix.wsgi:application
