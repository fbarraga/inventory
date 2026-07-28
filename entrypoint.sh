#!/bin/bash
set -e

echo "Waiting for database..."
max_attempts=30
attempt=0

while [ $attempt -lt $max_attempts ]; do
  if python -c "
import os
import psycopg2
try:
    conn = psycopg2.connect(
        host='$DB_HOST',
        database='$DB_NAME',
        user='$DB_USER',
        password='$DB_PASSWORD',
        connect_timeout=2
    )
    conn.close()
    exit(0)
except:
    exit(1)
" 2>/dev/null; then
    echo "Database is ready!"
    break
  fi
  attempt=$((attempt + 1))
  echo "Database not ready (attempt $attempt/$max_attempts), waiting..."
  sleep 1
done

if [ $attempt -ge $max_attempts ]; then
  echo "Database connection timed out after $max_attempts attempts"
  exit 1
fi

echo "Running migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting application..."
exec "$@"
