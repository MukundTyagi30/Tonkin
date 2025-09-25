#!/usr/bin/env python3
"""Setup script for Tonkin Knowledge Finder."""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"   Command: {command}")
        print(f"   Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is adequate."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8+ required, found {version.major}.{version.minor}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def main():
    """Main setup function."""
    print("🚀 Setting up Tonkin Knowledge Finder...")
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        print("\n💡 If you encounter issues, try:")
        print("   - Create a virtual environment: python -m venv venv")
        print("   - Activate it: source venv/bin/activate (Linux/Mac) or venv\\Scripts\\activate (Windows)")
        print("   - Then run this setup again")
        sys.exit(1)
    
    # Create necessary directories
    dirs_to_create = ["data", "embeddings", "data/processed"]
    for dir_name in dirs_to_create:
        Path(dir_name).mkdir(parents=True, exist_ok=True)
    print("✅ Created necessary directories")
    
    # Copy sample document to data directory if it exists
    sample_file = "SF84_Project_Basis_Report_V1.pdf"
    if os.path.exists(sample_file):
        import shutil
        shutil.copy(sample_file, "data/")
        print(f"✅ Copied {sample_file} to data/ directory")
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Add your SF84 documents to the 'data/' directory")
    print("2. Run: python ingest/create_index.py")
    print("3. Start the app: streamlit run app.py")
    print("\n💡 For help, see README.md or run commands with --help")

if __name__ == "__main__":
    main()
