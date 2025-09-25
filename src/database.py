"""Database operations for storing documents, embeddings, and feedback."""

import sqlite3
import json
import logging
from typing import List, Dict, Optional, Any
from datetime import datetime
from pathlib import Path

from config.settings import DATABASE_PATH

logger = logging.getLogger(__name__)


class KnowledgeDatabase:
    """SQLite database for storing documents, embeddings, and user feedback."""
    
    def __init__(self, db_path: str = None):
        self.db_path = db_path or DATABASE_PATH
        self.init_database()
    
    def init_database(self):
        """Initialize database tables."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Documents table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS documents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    file_path TEXT UNIQUE NOT NULL,
                    file_name TEXT NOT NULL,
                    file_size INTEGER,
                    created_date TEXT,
                    modified_date TEXT,
                    project_name TEXT,
                    project_number TEXT,
                    program_region TEXT,
                    category TEXT,
                    project_leader TEXT,
                    project_reviewer TEXT,
                    lead_disciplines TEXT,
                    client TEXT,
                    client_representative TEXT,
                    background TEXT,
                    scope_of_work TEXT,
                    scope_of_services TEXT,
                    deliverables TEXT,
                    reference_documents TEXT,
                    existing_concept_design TEXT,
                    assumptions TEXT,
                    performance_requirements TEXT,
                    operation_maintenance TEXT,
                    monitoring_controls TEXT,
                    trust_score REAL DEFAULT 0.0,
                    trust_badges TEXT,
                    searchable_text TEXT,
                    indexed_date TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Embeddings table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS embeddings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    document_id INTEGER,
                    section_name TEXT,
                    text_content TEXT,
                    embedding_vector BLOB,
                    created_date TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (document_id) REFERENCES documents (id)
                )
            """)
            
            # User feedback table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS feedback (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    document_id INTEGER,
                    search_query TEXT,
                    feedback_type TEXT,  -- 'thumbs_up', 'thumbs_down'
                    lesson_learned TEXT,
                    created_date TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (document_id) REFERENCES documents (id)
                )
            """)
            
            # Search history table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS search_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    query TEXT NOT NULL,
                    results_count INTEGER,
                    search_date TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.commit()
    
    def store_document(self, doc_data: Dict[str, Any]) -> int:
        """Store or update a document in the database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Convert trust_badges list to JSON string
            if 'trust_badges' in doc_data and isinstance(doc_data['trust_badges'], list):
                doc_data['trust_badges'] = json.dumps(doc_data['trust_badges'])
            
            # Check if document already exists
            cursor.execute("SELECT id FROM documents WHERE file_path = ?", (doc_data['file_path'],))
            existing = cursor.fetchone()
            
            if existing:
                # Update existing document
                doc_id = existing[0]
                
                # Build update query dynamically
                fields = []
                values = []
                for key, value in doc_data.items():
                    if key != 'file_path':  # Don't update the primary key
                        fields.append(f"{key} = ?")
                        values.append(value)
                
                values.append(doc_data['file_path'])  # For WHERE clause
                
                update_query = f"UPDATE documents SET {', '.join(fields)} WHERE file_path = ?"
                cursor.execute(update_query, values)
                
            else:
                # Insert new document
                fields = list(doc_data.keys())
                placeholders = ', '.join(['?' for _ in fields])
                values = [doc_data[field] for field in fields]
                
                insert_query = f"INSERT INTO documents ({', '.join(fields)}) VALUES ({placeholders})"
                cursor.execute(insert_query, values)
                doc_id = cursor.lastrowid
            
            conn.commit()
            return doc_id
    
    def get_document(self, doc_id: int) -> Optional[Dict[str, Any]]:
        """Retrieve a document by ID."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM documents WHERE id = ?", (doc_id,))
            row = cursor.fetchone()
            
            if row:
                doc = dict(row)
                # Parse trust_badges JSON
                if doc['trust_badges']:
                    try:
                        doc['trust_badges'] = json.loads(doc['trust_badges'])
                    except json.JSONDecodeError:
                        doc['trust_badges'] = []
                return doc
            
            return None
    
    def get_all_documents(self) -> List[Dict[str, Any]]:
        """Retrieve all documents."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM documents ORDER BY indexed_date DESC")
            rows = cursor.fetchall()
            
            documents = []
            for row in rows:
                doc = dict(row)
                # Parse trust_badges JSON
                if doc['trust_badges']:
                    try:
                        doc['trust_badges'] = json.loads(doc['trust_badges'])
                    except json.JSONDecodeError:
                        doc['trust_badges'] = []
                documents.append(doc)
            
            return documents
    
    def store_embedding(self, document_id: int, section_name: str, 
                       text_content: str, embedding_vector: bytes) -> int:
        """Store an embedding vector for a document section."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO embeddings (document_id, section_name, text_content, embedding_vector)
                VALUES (?, ?, ?, ?)
            """, (document_id, section_name, text_content, embedding_vector))
            
            conn.commit()
            return cursor.lastrowid
    
    def get_embeddings(self, document_id: int = None) -> List[Dict[str, Any]]:
        """Retrieve embeddings, optionally filtered by document ID."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            if document_id:
                cursor.execute("SELECT * FROM embeddings WHERE document_id = ?", (document_id,))
            else:
                cursor.execute("SELECT * FROM embeddings")
            
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    def store_feedback(self, document_id: int, search_query: str, 
                      feedback_type: str, lesson_learned: str = None) -> int:
        """Store user feedback for a document."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO feedback (document_id, search_query, feedback_type, lesson_learned)
                VALUES (?, ?, ?, ?)
            """, (document_id, search_query, feedback_type, lesson_learned))
            
            conn.commit()
            return cursor.lastrowid
    
    def get_feedback(self, document_id: int = None) -> List[Dict[str, Any]]:
        """Retrieve feedback, optionally filtered by document ID."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            if document_id:
                cursor.execute("SELECT * FROM feedback WHERE document_id = ? ORDER BY created_date DESC", (document_id,))
            else:
                cursor.execute("SELECT * FROM feedback ORDER BY created_date DESC")
            
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    def store_search(self, query: str, results_count: int) -> int:
        """Store search history."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO search_history (query, results_count)
                VALUES (?, ?)
            """, (query, results_count))
            
            conn.commit()
            return cursor.lastrowid
    
    def get_search_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Retrieve recent search history."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM search_history ORDER BY search_date DESC LIMIT ?", (limit,))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get database statistics."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            stats = {}
            
            # Document count
            cursor.execute("SELECT COUNT(*) FROM documents")
            stats['total_documents'] = cursor.fetchone()[0]
            
            # Embedding count
            cursor.execute("SELECT COUNT(*) FROM embeddings")
            stats['total_embeddings'] = cursor.fetchone()[0]
            
            # Feedback count
            cursor.execute("SELECT COUNT(*) FROM feedback")
            stats['total_feedback'] = cursor.fetchone()[0]
            
            # Average trust score
            cursor.execute("SELECT AVG(trust_score) FROM documents WHERE trust_score > 0")
            avg_score = cursor.fetchone()[0]
            stats['avg_trust_score'] = round(avg_score, 2) if avg_score else 0.0
            
            return stats
    
    def delete_document(self, document_id: int) -> bool:
        """Delete a document and all related data."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            try:
                # Delete related embeddings
                cursor.execute("DELETE FROM embeddings WHERE document_id = ?", (document_id,))
                
                # Delete related feedback
                cursor.execute("DELETE FROM feedback WHERE document_id = ?", (document_id,))
                
                # Delete document
                cursor.execute("DELETE FROM documents WHERE id = ?", (document_id,))
                
                conn.commit()
                return cursor.rowcount > 0
                
            except Exception as e:
                logger.error(f"Error deleting document {document_id}: {str(e)}")
                conn.rollback()
                return False


def main():
    """Test database operations."""
    db = KnowledgeDatabase()
    
    # Test document storage
    test_doc = {
        'file_path': '/test/sample.docx',
        'file_name': 'sample.docx',
        'file_size': 1024,
        'project_name': 'Test Project',
        'trust_score': 0.85,
        'trust_badges': ['Has Reviewer', 'Complete Header'],
        'searchable_text': 'This is test content for searching.'
    }
    
    doc_id = db.store_document(test_doc)
    print(f"Stored document with ID: {doc_id}")
    
    # Test retrieval
    retrieved = db.get_document(doc_id)
    print(f"Retrieved: {retrieved['project_name']}")
    
    # Test feedback
    feedback_id = db.store_feedback(doc_id, "test query", "thumbs_up", "This was helpful")
    print(f"Stored feedback with ID: {feedback_id}")
    
    # Show stats
    stats = db.get_stats()
    print(f"Database stats: {stats}")


if __name__ == "__main__":
    main()
