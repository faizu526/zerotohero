#!/usr/bin/env bash
# 🚀 Auto Build Script for Render

set -o errexit

echo "🔄 Starting build..."

pip install -r requirements.txt
mkdir -p staticfiles media

echo "🎨 Collecting static files..."
python manage.py collectstatic --no-input

echo "🗄️ Running migrations..."
python manage.py migrate --run-syncdb

echo "👤 Creating admin user..."
python manage.py shell << 'EOF'
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@zerotohero.com', 'admin123')
    print('✅ Admin created: admin/admin123')
EOF

echo "✅ Build complete!"
