"""Script to ingest documents and create search index."""

import os
import sys
import logging
from pathlib import Path

# Add src to path so we can import our modules
sys.path.append(str(Path(__file__).parent.parent / "src"))

from parser import DocumentParser, SF84Document
from database import KnowledgeDatabase
from search import SemanticSearchEngine
from utils import setup_logging, create_progress_callback, get_file_metadata

logger = logging.getLogger(__name__)


def ingest_documents(data_dir: str, force_rebuild: bool = False) -> int:
    """
    Ingest all supported documents from data directory.
    
    Args:
        data_dir: Directory containing documents to ingest
        force_rebuild: Whether to reprocess existing documents
    
    Returns:
        Number of documents successfully processed
    """
    data_path = Path(data_dir)
    if not data_path.exists():
        logger.error(f"Data directory not found: {data_dir}")
        return 0
    
    # Initialize components
    parser = DocumentParser()
    db = KnowledgeDatabase()
    
    # Find all supported files
    supported_files = []
    for ext in ['.docx', '.pdf']:
        supported_files.extend(data_path.glob(f"**/*{ext}"))
    
    if not supported_files:
        logger.warning(f"No supported files found in {data_dir}")
        return 0
    
    logger.info(f"Found {len(supported_files)} files to process")
    
    # Create progress callback
    progress = create_progress_callback(len(supported_files), "Ingesting documents")
    
    successful_count = 0
    
    for i, file_path in enumerate(supported_files):
        try:
            progress(i)
            
            # Check if already processed (unless force rebuild)
            if not force_rebuild:
                existing_docs = db.get_all_documents()
                if any(doc['file_path'] == str(file_path) for doc in existing_docs):
                    logger.debug(f"Skipping already processed: {file_path.name}")
                    continue
            
            logger.info(f"Processing: {file_path.name}")
            
            # Parse document
            doc = parser.parse_file(str(file_path))
            if doc is None:
                logger.warning(f"Failed to parse: {file_path.name}")
                continue
            
            # Store in database
            doc_data = doc.to_dict()
            doc_data['searchable_text'] = doc.get_searchable_text()
            
            doc_id = db.store_document(doc_data)
            logger.debug(f"Stored document with ID: {doc_id}")
            
            successful_count += 1
            
        except Exception as e:
            logger.error(f"Error processing {file_path.name}: {str(e)}")
            continue
    
    progress(len(supported_files))  # Complete progress
    
    logger.info(f"Successfully ingested {successful_count}/{len(supported_files)} documents")
    return successful_count


def create_search_index(force_rebuild: bool = False) -> bool:
    """
    Create or update the search index.
    
    Args:
        force_rebuild: Whether to rebuild index from scratch
    
    Returns:
        True if successful, False otherwise
    """
    logger.info("Creating search index...")
    
    search_engine = SemanticSearchEngine()
    
    success = search_engine.create_embeddings_for_documents(force_rebuild=force_rebuild)
    
    if success:
        stats = search_engine.get_index_stats()
        logger.info(f"Search index created successfully. Stats: {stats}")
    else:
        logger.error("Failed to create search index")
    
    return success


def main():
    """Main ingestion script."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Ingest documents and create search index")
    parser.add_argument(
        "--data-dir", 
        default="../data",
        help="Directory containing documents to ingest"
    )
    parser.add_argument(
        "--force-rebuild", 
        action="store_true",
        help="Force rebuild of existing documents and index"
    )
    parser.add_argument(
        "--log-level", 
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging level"
    )
    parser.add_argument(
        "--skip-indexing",
        action="store_true", 
        help="Skip creating search index (only ingest documents)"
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.log_level)
    
    # Get absolute path to data directory
    script_dir = Path(__file__).parent
    data_dir = (script_dir / args.data_dir).resolve()
    
    logger.info(f"Starting document ingestion from: {data_dir}")
    
    try:
        # Step 1: Ingest documents
        doc_count = ingest_documents(str(data_dir), args.force_rebuild)
        
        if doc_count == 0:
            logger.warning("No documents were ingested. Exiting.")
            return 1
        
        # Step 2: Create search index (unless skipped)
        if not args.skip_indexing:
            success = create_search_index(args.force_rebuild)
            if not success:
                logger.error("Failed to create search index")
                return 1
        
        logger.info("Ingestion completed successfully!")
        
        # Show final stats
        db = KnowledgeDatabase()
        stats = db.get_stats()
        logger.info(f"Database stats: {stats}")
        
        return 0
        
    except KeyboardInterrupt:
        logger.info("Ingestion interrupted by user")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return 1


if __name__ == "__main__":
    exit(main())
