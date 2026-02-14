#!/usr/bin/env python3
"""
🚀 Zero To Hero - FULL AUTO DEPLOYMENT
Usage: python auto_deploy.py
This script will automatically deploy your website to Render
"""

import os
import subprocess
import sys

def run_command(cmd, description, check=True):
    """Run a shell command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=check, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} complete!")
            return True, result.stdout
        else:
            if check:
                print(f"⚠️  {description} warning: {result.stderr}")
            return False, result.stderr
    except subprocess.CalledProcessError as e:
        print(f"❌ Error in {description}: {e}")
        if check:
            return False, str(e)
        return True, ""

def setup_render_yaml():
    """Ensure render.yaml is properly configured"""
    print("\n📋 Setting up render.yaml...")
    
    render_yaml_content = '''# 🚀 Render Deployment Configuration - FULLY AUTOMATED
# No manual setup required - everything is pre-configured

services:
  # Web Service - SQLite (No credit card required)
  - type: web
    name: zerotohero
    runtime: python
    plan: free
    autoDeploy: true
    buildCommand: "./build.sh"
    startCommand: "gunicorn config.wsgi:application"
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: DJANGO_SECRET_KEY
        generateValue: true
      - key: DEBUG
        value: "False"
      - key: USE_SQLITE
        value: "True"
      - key: WEB_CONCURRENCY
        value: "4"
      - key: RENDER_EXTERNAL_HOSTNAME
        value: zerotohero.onrender.com
      - key: BASE_URL
        value: https://zerotohero.onrender.com
'''
    
    with open('render.yaml', 'w') as f:
        f.write(render_yaml_content)
    
    print("✅ render.yaml configured")

def setup_build_script():
    """Ensure build.sh is executable and properly configured"""
    print("\n🔧 Setting up build.sh...")
    
    build_script = '''#!/usr/bin/env bash
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
'''
    
    with open('build.sh', 'w') as f:
        f.write(build_script)
    
    os.chmod('build.sh', 0o755)
    print("✅ build.sh configured")

def commit_and_push():
    """Commit all changes and push to GitHub"""
    print("\n📤 Pushing to GitHub...")
    
    run_command('git config user.email "deploy@zerotohero.com"', 'Git config', check=False)
    run_command('git config user.name "Auto Deploy"', 'Git config', check=False)
    run_command('git add -A', 'Adding files', check=False)
    
    success, _ = run_command('git commit -m "🚀 Auto-deploy: Full setup"', 'Committing', check=False)
    success, _ = run_command('git push origin main', 'Pushing', check=False)
    
    return success

def main():
    print("🚀 ZERO TO HERO - FULL AUTO DEPLOYMENT")
    print("="*60)
    
    if not os.path.exists('manage.py'):
        print("❌ Error: Run from project root")
        sys.exit(1)
    
    setup_render_yaml()
    setup_build_script()
    
    if commit_and_push():
        print("\n" + "="*60)
        print("🎉 READY! Go to:")
        print("   https://render.com/deploy?repo=https://github.com/faizu526/zerotohero")
        print("\n🔐 Admin: admin/admin123")
        print("="*60)
    else:
        print("\n⚠️  Push failed. Try: git push origin main")

if __name__ == '__main__':
    main()
