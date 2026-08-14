#!/bin/bash
set -e

echo "Running database migrations..."
python manage.py migrate --noinput

echo "Migrations completed successfully!"
echo "Starting gunicorn server..."
exec gunicorn gst_compliance_system.wsgi:application
