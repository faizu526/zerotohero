#!/usr/bin/env python3
"""
🚀 Auto Deploy Script for Render
Zero To Hero Django Project
"""

import os
import sys
import json
import subprocess
import time
import urllib.request
import urllib.error

# Colors for terminal output
GREEN = '\033[92m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
RED = '\033[91m'
ENDC = '\033[0m'

def print_step(step_num, message):
    print(f"\n{BLUE}[Step {step_num}]{ENDC} {message}")

def print_success(message):
    print(f"{GREEN}✅ {message}{ENDC}")

def print_warning(message):
    print(f"{YELLOW}⚠️  {message}{ENDC}")

def print_error(message):
    print(f"{RED}❌ {message}{ENDC}")

def run_command(cmd, description):
    """Run shell command and return output"""
    print(f"  Running: {cmd}")
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            capture_output=True, 
            text=True,
            timeout=60
        )
        if result.returncode == 0:
            print_success(f"{description} - Success!")
            return result.stdout.strip()
        else:
            print_error(f"{description} - Failed!")
            print(f"  Error: {result.stderr}")
            return None
    except subprocess.TimeoutExpired:
        print_error(f"{description} - Timeout!")
        return None
    except Exception as e:
        print_error(f"{description} - Error: {e}")
        return None

def check_git_repo():
    """Check if git repo is properly configured"""
    print_step(1, "Checking Git Repository")
    
    # Check if git is initialized
    if not os.path.exists('.git'):
        print_error("Git not initialized!")
        print("  Run: git init")
        return False
    
    # Check remote
    remote = run_command("git remote -v", "Check remote")
    if not remote or "github.com" not in remote:
        print_error("GitHub remote not found!")
        print("  Run: git remote add origin https://github.com/YOUR_USERNAME/zerotohero.git")
        return False
    
    print_success("Git repository configured correctly")
    return True

def push_to_github():
    """Push latest code to GitHub"""
    print_step(2, "Pushing to GitHub")
    
    # Add all files
    run_command("git add -A", "Add files")
    
    # Commit
    commit_msg = "Auto deploy - Render setup"
    run_command(f'git commit -m "{commit_msg}"', "Commit changes")
    
    # Push
    push_result = run_command("git push origin main", "Push to GitHub")
    
    if push_result is not None:
        print_success("Code pushed to GitHub!")
        return True
    return False

def generate_deploy_button():
    """Generate Deploy to Render button"""
    print_step(3, "Generating Deploy Button")
    
    repo_url = "https://github.com/faizu526/zerotohero"
    
    button_md = f"""
## 🚀 One-Click Deploy to Render

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo={repo_url})

**Click the button above to deploy automatically!**
"""
    
    # Save to file
    with open('DEPLOY_BUTTON.md', 'w') as f:
        f.write(button_md)
    
    print_success("Deploy button created!")
    print(f"\n{YELLOW}👉 Open this link in browser:{ENDC}")
    print(f"{BLUE}https://render.com/deploy?repo={repo_url}{ENDC}")
    
    return f"https://render.com/deploy?repo={repo_url}"

def create_deploy_script():
    """Create a shell script for deployment"""
    print_step(4, "Creating Deploy Script")
    
    script_content = """#!/bin/bash
# 🚀 Auto Deploy Script for Render

echo "🔄 Starting deployment..."

# Colors
GREEN='\\033[0;32m'
BLUE='\\033[0;34m'
NC='\\033[0m'

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
"""

    with open('deploy_render.sh', 'w') as f:
        f.write(script_content)
    
    # Make executable
    os.chmod('deploy_render.sh', 0o755)
    
    print_success("Deploy script created: deploy_render.sh")

def main():
    """Main deployment function"""
    print(f"\n{GREEN}{'='*60}{ENDC}")
    print(f"{GREEN}  🚀 ZERO TO HERO - AUTO DEPLOY TO RENDER{ENDC}")
    print(f"{GREEN}{'='*60}{ENDC}")
    
    # Check current directory
    if not os.path.exists('manage.py'):
        print_error("Not in Django project root directory!")
        print("  Please run from /home/redmoon/zerotohero")
        sys.exit(1)
    
    # Step 1: Check Git
    if not check_git_repo():
        print_error("Please fix git issues first!")
        sys.exit(1)
    
    # Step 2: Push to GitHub
    push_to_github()
    
    # Step 3: Generate deploy button
    deploy_url = generate_deploy_button()
    
    # Step 4: Create deploy script
    create_deploy_script()
    
    # Final output
    print(f"\n{GREEN}{'='*60}{ENDC}")
    print(f"{GREEN}  ✅ SETUP COMPLETE!{ENDC}")
    print(f"{GREEN}{'='*60}{ENDC}")
    print(f"\n{YELLOW}🎯 NEXT STEPS:{ENDC}")
    print(f"  1. Open this link in your browser:")
    print(f"     {BLUE}{deploy_url}{ENDC}")
    print(f"\n  2. Click 'Create Web Service' button")
    print(f"  3. Wait 5-10 minutes for deployment")
    print(f"\n{GREEN}  🌐 Your URL will be: https://zerotohero.onrender.com{ENDC}")
    print(f"\n{YELLOW}📋 Alternative:{ENDC}")
    print(f"  Run: {BLUE}./deploy_render.sh{ENDC} to deploy again")
    print(f"\n{GREEN}{'='*60}{ENDC}\n")

if __name__ == "__main__":
    main()
