"""Semantic search engine using sentence-transformers and FAISS."""

import os
import pickle
import numpy as np
import logging
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    SentenceTransformer = None

try:
    import faiss
except ImportError:
    faiss = None

from config.settings import (
    EMBEDDING_MODEL, 
    EMBEDDING_DIMENSION, 
    EMBEDDINGS_DIR, 
    MAX_SEARCH_RESULTS,
    SIMILARITY_THRESHOLD
)
from database import KnowledgeDatabase

logger = logging.getLogger(__name__)


class SemanticSearchEngine:
    """Semantic search engine for finding similar documents."""
    
    def __init__(self, model_name: str = None):
        self.model_name = model_name or EMBEDDING_MODEL
        self.model = None
        self.index = None
        self.document_map = {}  # Maps index positions to document IDs
        self.embeddings_file = EMBEDDINGS_DIR / "document_embeddings.pkl"
        self.index_file = EMBEDDINGS_DIR / "faiss_index.bin"
        self.map_file = EMBEDDINGS_DIR / "document_map.pkl"
        
        self.db = KnowledgeDatabase()
        
        # Ensure embeddings directory exists
        EMBEDDINGS_DIR.mkdir(parents=True, exist_ok=True)
    
    def _load_model(self):
        """Load the sentence transformer model."""
        if self.model is None:
            if SentenceTransformer is None:
                raise ImportError("sentence-transformers not available. Install with: pip install sentence-transformers")
            
            logger.info(f"Loading embedding model: {self.model_name}")
            self.model = SentenceTransformer(self.model_name)
    
    def _encode_text(self, text: str) -> np.ndarray:
        """Encode text into embedding vector."""
        self._load_model()
        return self.model.encode(text, convert_to_numpy=True)
    
    def _encode_texts(self, texts: List[str]) -> np.ndarray:
        """Encode multiple texts into embedding vectors."""
        self._load_model()
        return self.model.encode(texts, convert_to_numpy=True)
    
    def create_embeddings_for_documents(self, force_rebuild: bool = False) -> bool:
        """Create embeddings for all documents in the database."""
        if not force_rebuild and self._embeddings_exist():
            logger.info("Embeddings already exist. Use force_rebuild=True to recreate.")
            return True
        
        logger.info("Creating embeddings for all documents...")
        
        # Get all documents
        documents = self.db.get_all_documents()
        if not documents:
            logger.warning("No documents found in database")
            return False
        
        # Prepare texts for embedding
        texts = []
        doc_ids = []
        valid_docs = []
        
        for doc in documents:
            searchable_text = doc.get('searchable_text', '')
            if not searchable_text:
                # Try to construct searchable text from available fields
                text_parts = []
                for field in ['project_name', 'background', 'scope_of_work', 'deliverables']:
                    value = doc.get(field, '')
                    if value:
                        text_parts.append(str(value))
                searchable_text = ' '.join(text_parts)
            
            if searchable_text and len(searchable_text.strip()) > 10:  # Minimum text length
                texts.append(searchable_text)
                doc_ids.append(doc['id'])
                valid_docs.append(doc)
        
        if not texts:
            logger.error("No valid text content found in documents")
            return False
        
        try:
            # Generate embeddings
            logger.info(f"Generating embeddings for {len(texts)} documents...")
            embeddings = self._encode_texts(texts)
            
            # Create FAISS index
            if faiss is None:
                raise ImportError("faiss-cpu not available. Install with: pip install faiss-cpu")
            
            dimension = embeddings.shape[1]
            index = faiss.IndexFlatL2(dimension)  # L2 (Euclidean) distance
            index.add(embeddings.astype('float32'))
            
            # Create document mapping (index position -> document ID)
            document_map = {i: doc_id for i, doc_id in enumerate(doc_ids)}
            
            # Save everything
            self._save_embeddings(embeddings, index, document_map)
            
            logger.info(f"Successfully created embeddings for {len(texts)} documents")
            return True
            
        except Exception as e:
            logger.error(f"Error creating embeddings: {str(e)}")
            return False
    
    def _embeddings_exist(self) -> bool:
        """Check if embeddings files exist."""
        return (self.embeddings_file.exists() and 
                self.index_file.exists() and 
                self.map_file.exists())
    
    def _save_embeddings(self, embeddings: np.ndarray, index, document_map: Dict[int, int]):
        """Save embeddings, FAISS index, and document mapping to disk."""
        # Save embeddings
        with open(self.embeddings_file, 'wb') as f:
            pickle.dump(embeddings, f)
        
        # Save FAISS index
        faiss.write_index(index, str(self.index_file))
        
        # Save document mapping
        with open(self.map_file, 'wb') as f:
            pickle.dump(document_map, f)
        
        # Update instance variables
        self.index = index
        self.document_map = document_map
    
    def _load_embeddings(self) -> bool:
        """Load embeddings, FAISS index, and document mapping from disk."""
        try:
            if not self._embeddings_exist():
                return False
            
            # Load FAISS index
            if faiss is None:
                raise ImportError("faiss-cpu not available")
            
            self.index = faiss.read_index(str(self.index_file))
            
            # Load document mapping
            with open(self.map_file, 'rb') as f:
                self.document_map = pickle.load(f)
            
            logger.info(f"Loaded embeddings for {len(self.document_map)} documents")
            return True
            
        except Exception as e:
            logger.error(f"Error loading embeddings: {str(e)}")
            return False
    
    def search(self, query: str, top_k: int = None, threshold: float = None) -> List[Dict[str, Any]]:
        """Perform semantic search for similar documents."""
        top_k = top_k or MAX_SEARCH_RESULTS
        threshold = threshold or SIMILARITY_THRESHOLD
        
        # Load embeddings if not already loaded
        if self.index is None:
            if not self._load_embeddings():
                logger.error("No embeddings found. Please create embeddings first.")
                return []
        
        try:
            # Encode query
            query_embedding = self._encode_text(query)
            
            # Search FAISS index
            distances, indices = self.index.search(
                query_embedding.reshape(1, -1).astype('float32'), 
                top_k
            )
            
            # Convert distances to similarity scores (lower distance = higher similarity)
            similarities = 1 / (1 + distances[0])  # Convert L2 distance to similarity
            
            # Get results
            results = []
            for i, (idx, similarity) in enumerate(zip(indices[0], similarities)):
                if idx == -1:  # FAISS returns -1 for empty slots
                    continue
                
                # Apply similarity threshold
                if similarity < threshold:
                    continue
                
                # Get document ID and fetch document
                doc_id = self.document_map.get(idx)
                if doc_id is None:
                    continue
                
                document = self.db.get_document(doc_id)
                if document is None:
                    continue
                
                # Add search metadata
                document['similarity_score'] = float(similarity)
                document['search_rank'] = i + 1
                
                # Create text snippet
                searchable_text = document.get('searchable_text', '')
                snippet = self._create_snippet(searchable_text, query)
                document['snippet'] = snippet
                
                results.append(document)
            
            # Store search in history
            self.db.store_search(query, len(results))
            
            logger.info(f"Search for '{query}' returned {len(results)} results")
            return results
            
        except Exception as e:
            logger.error(f"Search error: {str(e)}")
            return []
    
    def _create_snippet(self, text: str, query: str, max_length: int = 200) -> str:
        """Create a relevant snippet from document text."""
        if not text or len(text) <= max_length:
            return text
        
        # Simple approach: find query terms and extract context
        query_words = query.lower().split()
        text_lower = text.lower()
        
        # Find the best position to extract snippet
        best_pos = 0
        max_matches = 0
        
        # Check every possible snippet position
        for i in range(0, len(text) - max_length, 50):  # Step by 50 chars
            snippet_text = text_lower[i:i + max_length]
            matches = sum(1 for word in query_words if word in snippet_text)
            if matches > max_matches:
                max_matches = matches
                best_pos = i
        
        # Extract snippet
        snippet = text[best_pos:best_pos + max_length]
        
        # Clean up snippet boundaries (avoid cutting words)
        if best_pos > 0:
            # Find start of word
            space_idx = snippet.find(' ')
            if space_idx > 0:
                snippet = snippet[space_idx + 1:]
        
        if best_pos + max_length < len(text):
            # Find end of word
            space_idx = snippet.rfind(' ')
            if space_idx > 0:
                snippet = snippet[:space_idx]
            snippet += "..."
        
        return snippet.strip()
    
    def get_index_stats(self) -> Dict[str, Any]:
        """Get statistics about the search index."""
        stats = {
            'embeddings_exist': self._embeddings_exist(),
            'index_loaded': self.index is not None,
            'total_documents': 0,
            'model_name': self.model_name
        }
        
        if self.index is not None:
            stats['total_documents'] = self.index.ntotal
        elif self.document_map:
            stats['total_documents'] = len(self.document_map)
        
        return stats
    
    def rebuild_index(self) -> bool:
        """Rebuild the search index from scratch."""
        logger.info("Rebuilding search index...")
        return self.create_embeddings_for_documents(force_rebuild=True)


def main():
    """Test the search engine."""
    search_engine = SemanticSearchEngine()
    
    # Create embeddings (if needed)
    print("Creating embeddings...")
    if search_engine.create_embeddings_for_documents():
        print("Embeddings created successfully")
        
        # Test search
        query = "stormwater detention SA"
        print(f"\nSearching for: '{query}'")
        results = search_engine.search(query, top_k=3)
        
        print(f"Found {len(results)} results:")
        for i, result in enumerate(results, 1):
            print(f"\n{i}. {result.get('project_name', 'Unknown Project')}")
            print(f"   Score: {result['similarity_score']:.3f}")
            print(f"   Snippet: {result['snippet'][:100]}...")
    else:
        print("Failed to create embeddings")
    
    # Show stats
    stats = search_engine.get_index_stats()
    print(f"\nIndex stats: {stats}")


if __name__ == "__main__":
    main()
