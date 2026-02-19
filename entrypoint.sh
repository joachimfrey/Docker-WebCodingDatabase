#!/bin/bash
set -e

echo "Starting Django application..."

# Wait for database to be ready
echo "Waiting for database..."
while ! nc -z $DB_HOST $DB_PORT 2>/dev/null; do
  echo "Database is unavailable - sleeping"
  sleep 1
done
echo "Database is up!"

# Run migrations
echo "Running migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Create logs directory
mkdir -p logs

echo "Application is ready!"
exec "$@"
