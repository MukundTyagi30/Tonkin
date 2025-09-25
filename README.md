# 🔍 Tonkin Knowledge Finder (SF84 MVP)

## Overview

A local, offline prototype that enables engineers to find trusted past projects in seconds by searching SF84 Project Basis Reports using semantic search technology.

## Key Features

- **Semantic Search**: Find projects by meaning, not just keywords
- **Trust Badges**: Automated quality indicators based on project metadata
- **Expert Network**: Identify project leaders and reviewers for knowledge sharing
- **Lesson Learned**: Capture and preserve project insights
- **Offline Operation**: All data stays local, no cloud dependencies
- **Tonkin Branding**: Professional UI with mobile responsiveness
- **Team Collaboration**: Expert finder and project sharing capabilities

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run setup
python setup.py

# Start the enhanced application
streamlit run app_enhanced.py
```

## Tech Stack

- **Frontend**: Streamlit with enhanced UI/UX
- **Search Engine**: Sentence Transformers + FAISS
- **Document Processing**: python-docx, PyMuPDF
- **Database**: SQLite
- **AI Models**: all-MiniLM-L6-v2

## Live Demo

🚀 **Access the live application**: [Tonkin Knowledge Finder](https://tonkin.streamlit.app)

## Project Structure

```
tonkin-knowledge-finder/
├── app_enhanced.py    # Main Streamlit application with enhanced UI
├── src/              # Core application logic
├── data/             # Document storage and processed data
├── config/           # Configuration settings
├── ingest/           # Document ingestion scripts
├── requirements.txt  # Python dependencies
└── README.md         # This file
```

## Documentation

- [Technical Documentation](README_TECHNICAL.md) - Detailed technical architecture
- [Executive Overview](README_EXECUTIVE.md) - Business value and vision
- [Deployment Guide](DEPLOYMENT_GUIDE.md) - Complete deployment options
- [Future Roadmap](FUTURE_ROADMAP.md) - Planned enhancements and features
- [Simple Explanation](SIMPLE_EXPLANATION.md) - Non-technical overview

## Sample Data

The prototype includes 20+ realistic sample projects covering:
- Stormwater management systems
- Bridge and infrastructure projects
- Water treatment facilities
- Renewable energy installations
- Industrial developments

## Features Showcase

### 🎨 Enhanced UI
- Professional Tonkin branding
- Mobile-responsive design
- Modern typography and visual effects
- Interactive dashboard with project analytics

### 🤝 Team Collaboration
- Expert finder by engineer name
- Contact project leaders and reviewers
- Project sharing capabilities
- Quick topic search for trending areas

### 🔍 Intelligent Search
- Semantic search understanding context
- Trust scoring based on project quality
- Advanced filtering and sorting options
- Highlighted search term matching

### 📊 Analytics Dashboard
- Project distribution by region and category
- Trust score analytics
- Search history and trending topics
- Performance metrics

## Contributing

This is a prototype for Tonkin Engineering. For questions or contributions, please contact the development team.

## License

Private prototype for Tonkin Engineering internal use.