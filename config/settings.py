"""Configuration settings for Tonkin Knowledge Finder."""

import os
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
EMBEDDINGS_DIR = PROCESSED_DATA_DIR / "embeddings"
DATABASE_PATH = PROCESSED_DATA_DIR / "knowledge_finder.db"

# Create directories if they don't exist
for dir_path in [RAW_DATA_DIR, PROCESSED_DATA_DIR, EMBEDDINGS_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

# Embedding model settings
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
EMBEDDING_DIMENSION = 384  # Dimension for all-MiniLM-L6-v2

# Search settings
MAX_SEARCH_RESULTS = 10
SIMILARITY_THRESHOLD = 0.3

# Trust scoring weights
TRUST_WEIGHTS = {
    "has_reviewer": 0.25,
    "complete_header": 0.20,
    "recent_document": 0.15,
    "standards_cited": 0.15,
    "region_present": 0.10,
    "revision_present": 0.10,
    "approval_stage": 0.05
}

# SF84 Document structure
SF84_HEADER_FIELDS = [
    "Project Name",
    "Project Number", 
    "Program/Region",
    "Category",
    "Project Leader",
    "Project Reviewer",
    "Lead Discipline(s)",
    "Client",
    "Client Representative"
]

SF84_SECTIONS = [
    "Background",
    "Scope of Work", 
    "Scope of Services",
    "Deliverables",
    "Reference documents & input data",
    "Existing concept design",
    "Assumptions",
    "Performance requirements",
    "Operation & maintenance",
    "Monitoring & controls"
]

# File type support
SUPPORTED_EXTENSIONS = [".docx", ".pdf"]
