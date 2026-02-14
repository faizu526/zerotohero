#!/bin/bash
# Start script for Railway deployment

# Run migrations
python manage.py migrate

# Start gunicorn
gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
