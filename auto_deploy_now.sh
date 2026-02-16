#!/usr/bin/env bash
# 🚀 AUTO DEPLOY SCRIPT - Zero To Hero
# Automatically deploys to Render with minimal manual steps

set -e

echo "🚀 ZERO TO HERO - AUTO DEPLOYMENT"
echo "=================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Step 1: Check Git status
print_status "Step 1: Checking Git status..."
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    print_error "Not a git repository!"
    echo "Run: git init"
    exit 1
fi

# Step 2: Check remote
print_status "Step 2: Checking GitHub remote..."
REMOTE=$(git remote get-url origin 2>/dev/null || echo "")
if [ -z "$REMOTE" ]; then
    print_warning "No GitHub remote found!"
    echo ""
    echo "👉 Manual step required:"
    echo "   1. Create repo on GitHub: https://github.com/new"
    echo "   2. Run these commands:"
    echo "      git remote add origin https://github.com/YOUR_USERNAME/zerotohero.git"
    echo "      git branch -M main"
    exit 1
else
    print_success "GitHub remote found: $REMOTE"
fi

# Step 3: Add all files
print_status "Step 3: Adding files to git..."
git add -A

# Step 4: Commit
print_status "Step 4: Committing changes..."
COMMIT_MSG="Deploy: Ready for Render with PostgreSQL"
if git diff --cached --quiet; then
    print_warning "No changes to commit"
else
    git commit -m "$COMMIT_MSG"
    print_success "Changes committed"
fi

# Step 5: Push
print_status "Step 5: Pushing to GitHub..."
if git push origin main; then
    print_success "Code pushed to GitHub!"
else
    print_error "Push failed!"
    echo "Try: git push -u origin main"
    exit 1
fi

echo ""
echo "=================================="
print_success "AUTO DEPLOY COMPLETE!"
echo "=================================="
echo ""
echo "🌐 NEXT STEPS (Manual - 2 minutes):"
echo "-----------------------------------"
echo ""
echo "1️⃣  Go to Render Dashboard:"
echo "   👉 https://dashboard.render.com"
echo ""
echo "2️⃣  Get your existing database URL:"
echo "   - Click 'PostgreSQL' in left sidebar"
echo "   - Select your existing database"
echo "   - Copy 'Internal Database URL'"
echo ""
echo "3️⃣  Create Web Service:"
echo "   - Click 'New +' → 'Web Service'"
echo "   - Select 'faizu526/zerotohero' repo"
echo "   - Click 'Connect'"
echo ""
echo "4️⃣  Set Environment Variables:"
echo "   - DATABASE_URL: (paste from step 2)"
echo "   - BASE_URL: https://zerotohero.onrender.com"
echo "   - USE_SQLITE: False"
echo ""
echo "5️⃣  Deploy:"
echo "   - Click 'Create Web Service'"
echo "   - Wait 5-10 minutes"
echo ""
echo "🎉 Your site will be live at: https://zerotohero.onrender.com"
echo ""
echo "📞 If you get 'database already exists' error:"
echo "   Use the existing database URL instead of creating new one"
echo ""
