from pathlib import Path
from typing import List, Dict, Any
import logging
from .document_loader import process_documents_directory as load_directory

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_documents_directory(directory_path: str) -> List[Dict[str, Any]]:
    """Process all documents in a directory using LangChain."""
    try:
        logger.info(f"Processing documents in directory: {directory_path}")
        processed_docs = load_directory(directory_path)
        logger.info(f"Successfully processed {len(processed_docs)} chunks from documents")
        return processed_docs
    except Exception as e:
        logger.error(f"Error processing directory {directory_path}: {str(e)}")
        raise
