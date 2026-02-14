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

# Create default superuser if none exists (for admin access)
python manage.py shell << 'EOF'
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@zerotohero.com', 'admin123')
    print('✅ Default superuser created: admin/admin123')
else:
    print('ℹ️ Superuser already exists')
EOF

echo "✅ Build complete!"
