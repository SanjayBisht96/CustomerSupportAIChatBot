from typing import List, Dict, Any
from pathlib import Path
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import logging

logger = logging.getLogger(__name__)

def process_documents_directory(directory_path: str) -> List[Dict[str, Any]]:
    """Process all documents in a directory using LangChain."""
    try:
        # Initialize DirectoryLoader with TextLoader for .txt files
        loader = DirectoryLoader(
            directory_path,
            glob="**/*.pdf",  
            loader_cls=PyPDFLoader,
            #loader_kwargs={'autodetect_encoding': True}
        )
        
        # Load documents
        documents = loader.load()
        logger.info(f"Loaded {len(documents)} documents from {directory_path}")
        
        # Initialize text splitter
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        
        # Split documents into chunks
        chunks = text_splitter.split_documents(documents)
        logger.info(f"Split documents into {len(chunks)} chunks")
        
        # Convert to required format
        processed_chunks = []
        for i, chunk in enumerate(chunks):
            processed_chunks.append({
                'text': chunk.page_content,
                'metadata': {
                    'source': Path(chunk.metadata['source']).name,
                    'chunk_id': i,
                    'file_type': '.pdf',
                    'path': chunk.metadata['source']
                }
            })
        
        return processed_chunks
        
    except Exception as e:
        logger.error(f"Error processing directory {directory_path}: {str(e)}")
        raise

def process_document(file_path: str) -> List[Dict[str, Any]]:
    """Process a single document using LangChain."""
    return process_documents_directory(str(Path(file_path).parent))
