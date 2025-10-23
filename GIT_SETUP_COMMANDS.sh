#!/bin/bash
# Git Repository Setup Script
# Run this step-by-step or all at once

echo "🚀 Git Repository Setup for QA Automation Framework"
echo "===================================================="
echo ""

# Step 1: Initialize Git
echo "Step 1: Initializing Git repository..."
git init
echo "✅ Git initialized"
echo ""

# Step 2: Configure Git (update with your details)
echo "Step 2: Configuring Git user..."
read -p "Enter your name: " git_name
read -p "Enter your email: " git_email
git config user.name "$git_name"
git config user.email "$git_email"
echo "✅ Git user configured"
echo ""

# Step 3: Add all files
echo "Step 3: Adding files to git..."
git add .
echo "✅ Files added"
echo ""

# Step 4: Show status
echo "Step 4: Checking git status..."
git status
echo ""

# Step 5: Create initial commit
echo "Step 5: Creating initial commit..."
git commit -m "Initial commit: QA Test Automation Framework

- Core framework with BasePage and BaseApiClient
- Team Alpha implementation (Google Shopping tests)
- Utility functions (string, wait, element helpers)
- Generic YAML data loader
- Parallel testing support with pytest-xdist
- Allure reporting integration
- Comprehensive documentation
- Makefile for common commands"
echo "✅ Initial commit created"
echo ""

# Step 6: Rename branch to main
echo "Step 6: Renaming branch to main..."
git branch -M main
echo "✅ Branch renamed to main"
echo ""

# Step 7: Add remote (user needs to update this)
echo "Step 7: Add remote origin..."
echo "⚠️  IMPORTANT: Update the remote URL below with your actual repository URL"
echo ""
echo "Choose your Git platform:"
echo "1) GitHub"
echo "2) GitLab"
echo "3) Company Git Server"
read -p "Enter choice (1-3): " platform_choice

case $platform_choice in
  1)
    read -p "Enter your GitHub username: " github_user
    read -p "Enter repository name (default: qa-automation-framework): " repo_name
    repo_name=${repo_name:-qa-automation-framework}
    remote_url="https://github.com/$github_user/$repo_name.git"
    ;;
  2)
    read -p "Enter your GitLab username: " gitlab_user
    read -p "Enter repository name (default: qa-automation-framework): " repo_name
    repo_name=${repo_name:-qa-automation-framework}
    remote_url="https://gitlab.com/$gitlab_user/$repo_name.git"
    ;;
  3)
    read -p "Enter your company Git server URL (e.g., git@git.company.com:team/repo.git): " remote_url
    ;;
  *)
    echo "Invalid choice"
    exit 1
    ;;
esac

echo ""
echo "Adding remote: $remote_url"
git remote add origin "$remote_url"
echo "✅ Remote added"
echo ""

# Step 8: Verify remote
echo "Step 8: Verifying remote..."
git remote -v
echo ""

# Step 9: Push to remote
echo "Step 9: Ready to push to remote"
echo "⚠️  Make sure you've created the PRIVATE repository on GitHub/GitLab first!"
read -p "Have you created the PRIVATE repository? (y/n): " confirm

if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
    echo "Pushing to remote..."
    git push -u origin main
    echo ""
    echo "✅ Successfully pushed to remote!"
else
    echo ""
    echo "⚠️  Please create the repository first, then run:"
    echo "   git push -u origin main"
fi

echo ""
echo "🎉 Git setup complete!"
echo ""
echo "Next steps:"
echo "1. Verify repository is PRIVATE on GitHub/GitLab"
echo "2. Add collaborators if needed"
echo "3. Set up branch protection rules (optional)"
echo "4. Configure CI/CD pipelines (optional)"
