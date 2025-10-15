#!/bin/bash

# 🚀 Quick Deploy Script for React Frontend
# This builds your React app and prepares it for deployment

echo "🚀 Tonkin Knowledge Finder - React Deployment"
echo "=============================================="
echo ""

# Check if we're in the frontend directory
if [ ! -f "package.json" ]; then
    echo "❌ Error: Run this script from the frontend/ directory"
    echo "   cd frontend && bash deploy.sh"
    exit 1
fi

echo "📦 Installing dependencies..."
npm install

if [ $? -ne 0 ]; then
    echo "❌ npm install failed"
    exit 1
fi

echo ""
echo "🔨 Building production bundle..."
npm run build

if [ $? -ne 0 ]; then
    echo "❌ Build failed"
    exit 1
fi

echo ""
echo "✅ Build successful!"
echo ""
echo "📁 Your production app is in: frontend/build/"
echo ""
echo "🌐 Next Steps - Choose one deployment method:"
echo ""
echo "Option 1️⃣ - Netlify Drag & Drop (Fastest):"
echo "   1. Go to: https://app.netlify.com/drop"
echo "   2. Drag the 'build' folder onto the page"
echo "   3. Your app goes live instantly!"
echo ""
echo "Option 2️⃣ - Netlify CLI:"
echo "   npm install -g netlify-cli"
echo "   netlify deploy --prod --dir=build"
echo ""
echo "Option 3️⃣ - Vercel:"
echo "   npm install -g vercel"
echo "   vercel --prod"
echo ""
echo "Option 4️⃣ - GitHub Pages:"
echo "   1. Push to GitHub"
echo "   2. Enable GitHub Pages in repo settings"
echo "   3. Set source to: gh-pages branch"
echo ""
echo "🎉 Ready to deploy!"

