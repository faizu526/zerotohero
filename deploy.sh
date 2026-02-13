#!/bin/bash
# 🚀 Quick Deploy Script for Zero To Hero

echo "🚀 Zero To Hero - Render Deployment Helper"
echo "=========================================="

# Check if git is initialized
if [ ! -d .git ]; then
    echo "❌ Git repository not found. Run: git init"
    exit 1
fi

# Check for uncommitted changes
if [ -n "$(git status --porcelain)" ]; then
    echo "📦 Uncommitted changes found. Committing..."
    git add .
    git commit -m "Update: $(date '+%Y-%m-%d %H:%M:%S')"
fi

# Check if remote exists
if ! git remote get-url origin &> /dev/null; then
    echo ""
    echo "🔗 GitHub Repository Setup Required!"
    echo "=================================="
    echo "1. Go to: https://github.com/new"
    echo "2. Repository name: zerotohero"
    echo "3. Click 'Create repository'"
    echo ""
    echo "Then run this command:"
    echo "git remote add origin https://github.com/YOUR_USERNAME/zerotohero.git"
    echo ""
    exit 1
fi

echo "📤 Pushing to GitHub..."
git push origin master || git push origin main

echo ""
echo "✅ Code pushed to GitHub!"
echo ""
echo "🌐 Next Steps for Render:"
echo "========================"
echo "1. Go to: https://render.com"
echo "2. Sign up with GitHub"
echo "3. Click 'New +' → 'Web Service'"
echo "4. Select 'zerotohero' repository"
echo "5. Click 'Connect'"
echo ""
echo "Render will auto-detect render.yaml and deploy!"
echo ""
echo "🌐 Your website will be at: https://zerotohero.onrender.com"
