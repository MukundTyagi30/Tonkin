# Tonkin Knowledge Finder (SF84 MVP)

A local, offline prototype that helps engineers find trusted past projects by searching SF84 Project Basis Reports using semantic search.

## Features

- 🔍 **Semantic Search**: Find documents by meaning, not just keywords
- 📊 **Trust Badges**: Automatic scoring based on completeness, approvals, and recency
- 👥 **Expert Network**: Identify project leaders and reviewers
- 💡 **Lessons Learned**: Capture and share insights from past projects
- 📱 **Modern UI**: Clean, intuitive Streamlit interface

## Quick Start

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Add your SF84 documents to `data/raw/`

3. Run the application:
```bash
streamlit run src/main.py
```

4. Open your browser to the displayed URL and start searching!

## Project Structure

```
tonkin-prototype/
├── data/
│   ├── raw/          # Original SF84 .docx files
│   └── processed/    # Parsed data and embeddings
├── src/
│   ├── main.py       # Streamlit app entry point
│   ├── parser.py     # Document parsing logic
│   ├── search.py     # Semantic search engine
│   ├── database.py   # SQLite database operations
│   └── utils.py      # Utility functions
├── config/
│   └── settings.py   # Configuration settings
└── requirements.txt
```

## Document Support

Currently supports:
- SF84 Project Basis Report (.docx)
- Future: Risk Register, PEP, Go/No-Go documents

## Technical Details

- **Embeddings**: sentence-transformers (all-MiniLM-L6-v2)
- **Vector Search**: FAISS CPU
- **Database**: SQLite for feedback and lessons
- **UI**: Streamlit
- **Platform**: Windows/Mac compatible
