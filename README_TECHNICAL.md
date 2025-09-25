# Tonkin Knowledge Finder - Technical Documentation

## 🚀 System Overview

The Tonkin Knowledge Finder is an AI-powered prototype that demonstrates semantic search capabilities for engineering project documentation. It transforms traditional keyword-based document search into intelligent, meaning-based discovery using natural language processing and machine learning.

## 🏗️ Architecture & Technology Stack

### Core Technologies
- **Python 3.8+**: Primary development language
- **Streamlit**: Web UI framework for rapid prototyping
- **sentence-transformers**: AI embeddings (all-MiniLM-L6-v2 model)
- **FAISS**: Facebook AI Similarity Search for vector indexing
- **SQLite**: Local database for metadata and user feedback
- **python-docx**: Microsoft Word document parsing
- **PyPDF2**: PDF document parsing
- **Plotly**: Interactive data visualizations

### System Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Document      │    │   AI Processing  │    │   Search &      │
│   Ingestion     │───▶│   Pipeline       │───▶│   User Interface│
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│ • .docx Parser  │    │ • Text Embedding │    │ • Semantic      │
│ • .pdf Parser   │    │ • Vector Index   │    │   Search        │
│ • Metadata      │    │ • FAISS Storage  │    │ • Result Cards  │
│   Extraction    │    │ • Trust Scoring  │    │ • Feedback Loop │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                     SQLite Database                            │
│  ├── Documents (metadata, text, trust scores)                 │
│  ├── Embeddings (vector representations)                      │
│  ├── Feedback (user ratings, lessons learned)                 │
│  └── Search History (query analytics)                         │
└─────────────────────────────────────────────────────────────────┘
```

## 📄 Current Document Processing Capabilities

### SF84 Project Basis Report Parser
The prototype currently processes SF84 Project Basis Reports with sophisticated metadata extraction:

**Header Fields Extracted:**
- Project Name, Number, Region, Category
- Project Leader, Reviewer, Lead Disciplines
- Client, Client Representative

**Content Sections Parsed:**
- Background, Scope of Work, Scope of Services
- Deliverables, Reference Documents, Assumptions
- Performance Requirements, O&M, Monitoring & Controls

**Technical Implementation:**
```python
# Document parsing pipeline
def parse_sf84_document(file_path):
    doc = Document(file_path)  # python-docx
    
    # Extract structured metadata
    metadata = extract_header_fields(doc)
    
    # Parse content sections
    sections = extract_content_sections(doc)
    
    # Calculate trust score
    trust_score = calculate_trust_metrics(metadata, sections)
    
    return SF84Document(metadata, sections, trust_score)
```

## 🧠 AI & Machine Learning Components

### Semantic Embeddings
- **Model**: all-MiniLM-L6-v2 (384-dimensional vectors)
- **Purpose**: Convert text into numerical representations that capture meaning
- **Advantage**: "SA" matches "South Australia", "detention" matches "stormwater basin"

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(document_texts)  # Convert to vectors
```

### Vector Search with FAISS
- **Index Type**: L2 (Euclidean distance) for similarity matching
- **Performance**: Sub-millisecond search across thousands of documents
- **Scalability**: Can handle millions of documents with proper hardware

```python
import faiss

# Create and populate vector index
dimension = 384
index = faiss.IndexFlatL2(dimension)
index.add(embeddings.astype('float32'))

# Perform semantic search
query_vector = model.encode(user_query)
distances, indices = index.search(query_vector, top_k=10)
```

### Trust Scoring Algorithm
Automated quality assessment based on document completeness and metadata:

```python
def calculate_trust_score(document):
    score = 0.0
    
    # Reviewer present (25% weight)
    if document.project_reviewer:
        score += 0.25
    
    # Header completeness (20% weight)
    required_fields = ['project_name', 'project_number', 'client']
    if all(getattr(document, field) for field in required_fields):
        score += 0.20
    
    # Content completeness (15% weight)
    content_sections = ['background', 'scope_of_work', 'deliverables']
    if all(getattr(document, section) for section in content_sections):
        score += 0.15
    
    # Additional factors: recency, standards, region (40% weight)
    score += calculate_additional_factors(document)
    
    return min(score, 1.0)
```

## 🗃️ Database Schema

### Documents Table
```sql
CREATE TABLE documents (
    id INTEGER PRIMARY KEY,
    file_path TEXT UNIQUE,
    project_name TEXT,
    project_number TEXT,
    program_region TEXT,
    project_leader TEXT,
    project_reviewer TEXT,
    trust_score REAL,
    trust_badges TEXT,  -- JSON array
    searchable_text TEXT,
    indexed_date TIMESTAMP
);
```

### Embeddings Table
```sql
CREATE TABLE embeddings (
    id INTEGER PRIMARY KEY,
    document_id INTEGER,
    text_content TEXT,
    embedding_vector BLOB,  -- Serialized numpy array
    FOREIGN KEY (document_id) REFERENCES documents(id)
);
```

## 🔍 Search Pipeline

### 1. Query Processing
```python
def semantic_search(query, top_k=10, threshold=0.3):
    # Convert query to vector
    query_embedding = model.encode(query)
    
    # Search FAISS index
    distances, indices = index.search(query_embedding, top_k)
    
    # Convert distances to similarity scores
    similarities = 1 / (1 + distances[0])
    
    # Filter by threshold and retrieve documents
    results = []
    for idx, similarity in zip(indices[0], similarities):
        if similarity >= threshold:
            doc = database.get_document(document_map[idx])
            doc['similarity_score'] = similarity
            results.append(doc)
    
    return results
```

### 2. Result Ranking
- **Primary**: Semantic similarity score
- **Secondary**: Trust score weighting
- **Tertiary**: Recency and user feedback

### 3. Snippet Generation
```python
def create_snippet(text, query, max_length=200):
    # Find query terms in text
    query_words = query.lower().split()
    
    # Locate best excerpt position
    best_position = find_best_match_position(text, query_words)
    
    # Extract and clean snippet
    snippet = extract_clean_snippet(text, best_position, max_length)
    
    return snippet
```

## 📊 Current Prototype Limitations & Future Enhancements

### Current State (Prototype v1.0)
**Document Types**: SF84 Project Basis Reports only
**Volume**: 23 sample documents across 8 Australian states
**File Formats**: .docx and .pdf (basic extraction)
**Search Scope**: Full document text with basic metadata

### Identified Limitations

#### 1. **Limited Document Template Support**
```python
# Current: Single template parser
parser = SF84Parser()

# Future: Multi-template system
parsers = {
    'SF84': SF84Parser(),
    'Risk_Register': RiskRegisterParser(),
    'PEP': PEPParser(),
    'Go_No_Go': GoNoGoParser(),
    'Design_Review': DesignReviewParser()
}
```

#### 2. **Basic PDF Processing**
```python
# Current: Simple text extraction
text = extract_text_from_pdf(file_path)

# Future: OCR + layout analysis
text = ocr_engine.extract_with_layout(file_path)
structured_data = layout_analyzer.parse_sections(text)
```

#### 3. **No File Opening Integration**
```python
# Current: Basic file opening
os.startfile(file_path)  # Windows only

# Future: Document viewer integration
viewer = DocumentViewer()
viewer.open_with_highlighting(file_path, search_terms)
viewer.jump_to_section(section_name)
```

## 🚀 Scaling Strategies

### For Production Deployment

#### 1. **Multi-Document Template System with Project Relationships**
```python
class ProjectDocumentManager:
    def __init__(self):
        self.parsers = {
            'SF84_PROJECT_BASIS': SF84Parser(),
            'RISK_REGISTER': RiskRegisterParser(),
            'PEP': PEPParser(),
            'GO_NO_GO': GoNoGoParser(),
            'DESIGN_REVIEW': DesignReviewParser(),
            'SITE_PLAN': SitePlanParser(),
            'PHOTO_DOCUMENTATION': PhotoParser(),
            'TECHNICAL_SPECIFICATION': TechnicalSpecParser()
        }
    
    def create_project_knowledge_graph(self, project_number):
        """Link all documents belonging to the same project"""
        project_docs = self.find_project_documents(project_number)
        
        # Create relationships between document types
        relationships = {
            'core_project': project_docs.get('SF84_PROJECT_BASIS'),
            'risk_analysis': project_docs.get('RISK_REGISTER'),
            'feasibility': project_docs.get('PEP', project_docs.get('GO_NO_GO')),
            'technical_reviews': project_docs.get('DESIGN_REVIEW', []),
            'site_context': project_docs.get('SITE_PLAN', []),
            'visual_documentation': project_docs.get('PHOTO_DOCUMENTATION', []),
            'specifications': project_docs.get('TECHNICAL_SPECIFICATION', [])
        }
        
        return ProjectKnowledgeGraph(project_number, relationships)
```

#### 2. **Enhanced PDF Processing**
```python
# OCR for scanned documents
import pytesseract
from pdf2image import convert_from_path

def advanced_pdf_processing(file_path):
    # Try text extraction first
    text = extract_text_layer(file_path)
    
    if not text or len(text) < 100:
        # Fallback to OCR
        images = convert_from_path(file_path)
        text = ""
        for image in images:
            text += pytesseract.image_to_string(image)
    
    return text
```

#### 3. **Distributed Vector Storage**
```python
# Current: Local FAISS
index = faiss.IndexFlatL2(dimension)

# Production: Distributed vector database
from weaviate import Client

client = Client("http://weaviate-cluster:8080")
# Supports billions of vectors with real-time updates
```

#### 4. **Document Management Integration**
```python
class SharePointConnector:
    def sync_documents(self, site_url, library_name):
        # Automated document discovery
        new_docs = self.get_new_documents(since_last_sync)
        
        for doc in new_docs:
            # Parse and index automatically
            parsed = self.parser_factory.parse(doc)
            self.vector_store.add_document(parsed)
```

## 📈 Performance Characteristics

### Current Prototype Metrics
- **Index Build Time**: ~30 seconds for 23 documents
- **Search Latency**: <100ms for top-10 results
- **Memory Usage**: ~200MB for loaded model + index
- **Storage**: ~5MB for 23 documents + embeddings

### Production Scaling Estimates
```python
# Linear scaling characteristics
documents = 10000
estimated_metrics = {
    'index_build_time': f'{documents * 1.3 / 1000:.1f} minutes',
    'search_latency': '<200ms',  # FAISS scales well
    'memory_usage': f'{200 + (documents * 0.5)}MB',
    'storage_size': f'{documents * 0.2}MB'
}
```

## 🔧 Development & Deployment

### Local Development Setup
```bash
# Clone and setup
git clone <repository>
cd tonkin-knowledge-finder

# Install dependencies
pip install -r requirements.txt

# Initialize sample data
python create_expanded_data.py

# Build search index
python ingest/create_index.py

# Start application
streamlit run app_enhanced.py
```

### Docker Deployment
```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8501

CMD ["streamlit", "run", "app_enhanced.py", "--server.address", "0.0.0.0"]
```

### Environment Configuration
```python
# config/production.py
DATABASE_URL = "postgresql://user:pass@db:5432/tonkin_kb"
VECTOR_STORE_URL = "http://weaviate:8080"
DOCUMENT_STORE_PATH = "/mnt/sharepoint/documents"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # or larger model for production

# Performance tuning
SEARCH_CACHE_TTL = 300  # 5 minutes
MAX_SEARCH_RESULTS = 50
SIMILARITY_THRESHOLD = 0.2
```

## 🔒 Security & Compliance Considerations

### Data Privacy
- **Local Processing**: No data sent to external APIs
- **Encryption**: SQLite database encryption for sensitive projects
- **Access Control**: User authentication and authorization layers

### Document Discovery & Ingestion Strategy

#### Addressing Tonkin's Current Storage Challenges
```python
class DocumentDiscoveryEngine:
    """
    Handles document discovery across multiple unorganized storage locations
    """
    
    def discover_project_documents(self, scan_locations):
        """
        Intelligent document discovery for organizations without 
        centralized document management
        """
        discovered_projects = {}
        
        for location in scan_locations:
            # Scan network drives, local folders, email attachments
            files = self.recursive_file_scan(location)
            
            for file_path in files:
                # Auto-detect project number from filename/content
                project_number = self.extract_project_number(file_path)
                
                if project_number:
                    # Group documents by project
                    if project_number not in discovered_projects:
                        discovered_projects[project_number] = []
                    
                    doc_info = {
                        'file_path': file_path,
                        'doc_type': self.classify_document_type(file_path),
                        'last_modified': self.get_file_stats(file_path),
                        'extracted_metadata': self.quick_metadata_scan(file_path)
                    }
                    
                    discovered_projects[project_number].append(doc_info)
        
        return discovered_projects
    
    def extract_project_number(self, file_path):
        """
        Extract project numbers from various naming conventions:
        - TKN-2024-SW-001_Risk_Register.pdf
        - Project_Basis_Report_TKN2024SW001.docx  
        - 2024-001-Site-Photos.zip
        """
        patterns = [
            r'TKN[-_]?(\d{4})[-_]?([A-Z]{2,3})[-_]?(\d{3})',
            r'(\d{4})[-_](\d{3})[-_]',
            r'Project[_\s](\d+)',
        ]
        
        filename = os.path.basename(file_path)
        for pattern in patterns:
            match = re.search(pattern, filename, re.IGNORECASE)
            if match:
                return self.normalize_project_number(match.groups())
        
        # Also scan file content for project numbers
        return self.scan_content_for_project_number(file_path)

# Document Type Classification
DOCUMENT_PATTERNS = {
    'SF84_PROJECT_BASIS': [
        'project_basis', 'SF84', 'project_definition',
        'scope_of_work', 'project_brief'
    ],
    'RISK_REGISTER': [
        'risk_register', 'risk_assessment', 'hazard_analysis',
        'risk_matrix', 'risk_management'
    ],
    'PEP': [
        'project_execution_plan', 'PEP', 'execution_plan',
        'project_plan', 'delivery_plan'
    ],
    'GO_NO_GO': [
        'go_no_go', 'decision_gate', 'gate_review',
        'feasibility_decision', 'project_approval'
    ],
    'DESIGN_REVIEW': [
        'design_review', 'technical_review', 'peer_review',
        'design_check', 'quality_review'
    ],
    'SITE_PLAN': [
        'site_plan', 'layout', 'general_arrangement',
        'site_layout', 'masterplan', 'drawing'
    ],
    'PHOTO_DOCUMENTATION': [
        'photo', 'image', 'site_visit', 'inspection',
        'progress_photos', 'documentation'
    ]
}
```

### Document Security & Access Control
```python
class SecureDocumentAccess:
    def check_permissions(self, user, document):
        # Project-level access control
        if document.classification == 'CONFIDENTIAL':
            return user.has_clearance('CONFIDENTIAL')
        
        # Client-specific restrictions  
        if document.client in user.restricted_clients:
            return False
        
        return True
    
    def audit_document_access(self, user, document, action):
        """Track who accesses what documents for compliance"""
        audit_log = {
            'user': user.id,
            'document': document.id,
            'action': action,
            'timestamp': datetime.now(),
            'ip_address': self.get_client_ip()
        }
        self.audit_database.log_access(audit_log)
```

## 📊 Analytics & Monitoring

### Search Analytics
```python
def track_search_metrics(query, results, user_feedback):
    metrics = {
        'query': query,
        'result_count': len(results),
        'avg_similarity': np.mean([r['similarity_score'] for r in results]),
        'user_satisfaction': user_feedback,
        'timestamp': datetime.now()
    }
    
    analytics_db.store_metrics(metrics)
```

### System Health Monitoring
- **Index Freshness**: Last update timestamps
- **Search Performance**: P95 latency tracking
- **User Engagement**: Click-through rates, feedback scores
- **Document Coverage**: Parsing success rates by document type

## 🎯 Next Steps for Production

1. **Document Template Expansion**: Add parsers for Risk Registers, PEPs, Design Reviews
2. **SharePoint Integration**: Automated document discovery and indexing
3. **Advanced PDF Processing**: OCR, table extraction, drawing analysis
4. **User Authentication**: Integration with corporate SSO
5. **Advanced Analytics**: Search behavior analysis, recommendation engine
6. **Mobile Interface**: Responsive design for field engineers
7. **API Development**: RESTful API for integration with other tools

This technical foundation provides a scalable, maintainable platform for enterprise knowledge management with the flexibility to evolve with Tonkin's growing documentation needs.
