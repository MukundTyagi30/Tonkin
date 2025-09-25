#!/bin/bash

# 🚀 Quick Deployment to Streamlit Community Cloud
# This script helps you deploy to Streamlit Cloud in minutes

echo "🚀 Tonkin Knowledge Finder - Quick Deployment Script"
echo "==============================================="

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📁 Initializing Git repository..."
    git init
    git add .
    git commit -m "Initial commit: Tonkin Knowledge Finder with enhanced UI and team collaboration"
else
    echo "✅ Git repository already initialized"
fi

# Check for GitHub remote
if ! git remote get-url origin &> /dev/null; then
    echo ""
    echo "🔗 GitHub Setup Required:"
    echo "1. Go to https://github.com/new"
    echo "2. Create a new repository named: tonkin-knowledge-finder"
    echo "3. Copy the repository URL"
    echo ""
    read -p "Enter your GitHub repository URL: " repo_url
    git remote add origin "$repo_url"
fi

echo ""
echo "📤 Pushing to GitHub..."
git add .
git commit -m "Enhanced UI with Tonkin branding and team collaboration features" 2>/dev/null || echo "No changes to commit"
git push -u origin main

echo ""
echo "🌐 Streamlit Cloud Deployment:"
echo "1. Go to https://share.streamlit.io"
echo "2. Click 'New app'"
echo "3. Connect your GitHub account"
echo "4. Select your repository: tonkin-knowledge-finder"
echo "5. Main file path: app_enhanced.py"
echo "6. Click 'Deploy!'"
echo ""
echo "⏱️  Deployment will take 3-5 minutes"
echo "📱 Your app will be available at: https://tonkin-knowledge-finder.streamlit.app"
echo ""
echo "✅ Deployment preparation complete!"
echo "📖 See DEPLOYMENT_GUIDE.md for more deployment options"
