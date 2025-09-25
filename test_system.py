#!/usr/bin/env python3
"""Test script to verify Tonkin Knowledge Finder components."""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

def test_imports():
    """Test that all modules can be imported."""
    print("🧪 Testing imports...")
    
    try:
        from parser import DocumentParser
        print("✅ Parser module imported")
    except Exception as e:
        print(f"❌ Parser import failed: {e}")
        return False
    
    try:
        from database import KnowledgeDatabase
        print("✅ Database module imported")
    except Exception as e:
        print(f"❌ Database import failed: {e}")
        return False
    
    try:
        from search import SemanticSearchEngine
        print("✅ Search module imported")
    except Exception as e:
        print(f"❌ Search import failed: {e}")
        return False
    
    try:
        from utils import open_file, format_date
        print("✅ Utils module imported")
    except Exception as e:
        print(f"❌ Utils import failed: {e}")
        return False
    
    return True

def test_document_parsing():
    """Test document parsing with sample file."""
    print("\n📄 Testing document parsing...")
    
    try:
        from parser import DocumentParser
        
        parser = DocumentParser()
        sample_file = "data/SF84_Project_Basis_Report_V1.pdf"
        
        if not os.path.exists(sample_file):
            print(f"⚠️ Sample file not found: {sample_file}")
            return True  # Not a failure, just no test file
        
        print(f"   Parsing: {sample_file}")
        doc = parser.parse_file(sample_file)
        
        if doc:
            print(f"✅ Successfully parsed document")
            print(f"   File: {doc.file_name}")
            print(f"   Size: {doc.file_size} bytes")
            print(f"   Trust Score: {doc.trust_score:.2f}")
            print(f"   Trust Badges: {', '.join(doc.trust_badges)}")
            searchable_length = len(doc.get_searchable_text())
            print(f"   Searchable text: {searchable_length} characters")
            return True
        else:
            print(f"❌ Failed to parse document")
            return False
            
    except Exception as e:
        print(f"❌ Document parsing test failed: {e}")
        return False

def test_database():
    """Test database operations."""
    print("\n🗄️ Testing database...")
    
    try:
        from database import KnowledgeDatabase
        
        db = KnowledgeDatabase()
        print("✅ Database initialized")
        
        # Test basic operations
        stats = db.get_stats()
        print(f"   Stats: {stats}")
        
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def test_search_engine():
    """Test search engine initialization."""
    print("\n🔍 Testing search engine...")
    
    try:
        from search import SemanticSearchEngine
        
        search_engine = SemanticSearchEngine()
        print("✅ Search engine initialized")
        
        stats = search_engine.get_index_stats()
        print(f"   Index stats: {stats}")
        
        return True
        
    except Exception as e:
        print(f"❌ Search engine test failed: {e}")
        return False

def check_dependencies():
    """Check if required dependencies are available."""
    print("\n📦 Checking dependencies...")
    
    dependencies = {
        'docx': 'python-docx',
        'PyPDF2': 'PyPDF2', 
        'sentence_transformers': 'sentence-transformers',
        'faiss': 'faiss-cpu',
        'streamlit': 'streamlit',
        'pandas': 'pandas'
    }
    
    missing = []
    
    for module, package in dependencies.items():
        try:
            __import__(module)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} (missing)")
            missing.append(package)
    
    if missing:
        print(f"\n💡 Install missing packages with:")
        print(f"   pip install {' '.join(missing)}")
        return False
    
    return True

def main():
    """Run all tests."""
    print("🚀 Tonkin Knowledge Finder - System Test\n")
    
    all_passed = True
    
    # Check dependencies first
    if not check_dependencies():
        print("\n❌ Dependency check failed. Install missing packages and try again.")
        return False
    
    # Test imports
    if not test_imports():
        all_passed = False
    
    # Test database
    if not test_database():
        all_passed = False
    
    # Test document parsing
    if not test_document_parsing():
        all_passed = False
    
    # Test search engine
    if not test_search_engine():
        all_passed = False
    
    print("\n" + "="*50)
    if all_passed:
        print("🎉 All tests passed! System is ready.")
        print("\n📋 Next steps:")
        print("1. Run: python ingest/create_index.py")
        print("2. Start app: streamlit run app.py")
    else:
        print("❌ Some tests failed. Check errors above.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
