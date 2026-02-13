#!/bin/bash
# 🚀 Auto Deploy Script for Render

echo "🔄 Starting deployment..."

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}Step 1: Checking GitHub repo...${NC}"
git status

echo -e "${BLUE}Step 2: Pushing latest code...${NC}"
git add -A
git commit -m "Deploy: $(date)" || echo "No changes to commit"
git push origin main

echo -e "${GREEN}✅ Code pushed to GitHub!${NC}"
echo ""
echo -e "${BLUE}👉 Now open this link to deploy:${NC}"
echo -e "${GREEN}https://render.com/deploy?repo=https://github.com/faizu526/zerotohero${NC}"
echo ""
echo "Click 'Create Web Service' and your site will be live!"
