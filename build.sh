#!/usr/bin/env bash
# 🚀 Build Script for Render Deployment

set -o errexit

echo "🔄 Starting build..."

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate

echo "✅ Build complete!"
