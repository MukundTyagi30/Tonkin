#!/bin/bash

# Tonkin Knowledge Finder - Quick Start Script

echo "🚀 Tonkin Knowledge Finder - Quick Start"
echo "========================================"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8+ and try again."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo "❌ app.py not found. Please run this script from the project root directory."
    exit 1
fi

# Step 1: Install dependencies
echo ""
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies. Try creating a virtual environment:"
    echo "   python3 -m venv venv"
    echo "   source venv/bin/activate"
    echo "   pip install -r requirements.txt"
    exit 1
fi

# Step 2: Test the system
echo ""
echo "🧪 Testing system components..."
python3 test_system.py

if [ $? -ne 0 ]; then
    echo "❌ System test failed. Check the error messages above."
    exit 1
fi

# Step 3: Check for documents
if [ ! "$(ls -A data/*.pdf data/*.docx 2>/dev/null)" ]; then
    echo ""
    echo "⚠️  No documents found in data/ directory."
    echo "   Add some .docx or .pdf files to data/ and run:"
    echo "   python3 ingest/create_index.py"
    echo ""
else
    echo ""
    echo "📄 Found documents in data/ directory. Creating search index..."
    python3 ingest/create_index.py
    
    if [ $? -ne 0 ]; then
        echo "❌ Failed to create search index."
        exit 1
    fi
fi

# Step 4: Start the application
echo ""
echo "🎉 Setup complete! Starting Tonkin Knowledge Finder..."
echo ""
echo "💡 The app will open in your browser. If it doesn't, go to:"
echo "   http://localhost:8501"
echo ""
echo "🔍 Try searching for:"
echo "   - 'stormwater detention'"
echo "   - 'bridge design'"
echo "   - 'SA projects'"
echo ""

# Start Streamlit
streamlit run app.py
