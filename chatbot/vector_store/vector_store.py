from typing import List, Dict, Any
import chromadb
from chromadb.config import Settings
import openai
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class VectorStore:
    def __init__(self, persist_directory: str = "chroma_db"):
        # Initialize ChromaDB
        self.client = chromadb.Client(Settings(
            persist_directory=persist_directory,
            anonymized_telemetry=False
        ))
        
        # Create or get collection
        self.collection = self.client.get_or_create_collection(
            name="insurance_docs",
            metadata={"hnsw:space": "cosine"}
        )
        
        # Initialize OpenAI client
        self.openai_client = openai.OpenAI(
                                    api_key=os.getenv('OPENAI_API_KEY_EMBEDDING'),
                                    base_url=os.getenv('EMBEDDING_ENDPOINT')
        )
        
    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Get embeddings using OpenAI API."""
        try:
            response = self.openai_client.embeddings.create(
                model="text-embedding-3-small",
                input=texts
            )
            return [embedding.embedding for embedding in response.data]
        except Exception as e:
            print(f"Error getting embeddings: {e}")
            raise

    def add_documents(self, documents: List[Dict[str, Any]]) -> None:
        """Add documents to the vector store."""
        texts = [doc['text'] for doc in documents]
        ids = [f"doc_{i}" for i in range(len(documents))]
        embeddings = self.get_embeddings(texts)
        metadatas = [doc['metadata'] for doc in documents]

        # Add to ChromaDB
        self.collection.add(
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )

    def similarity_search(self, query: str, k: int = 3) -> List[Dict[str, Any]]:
        """Search for similar documents."""
        # Generate query embedding
        query_embedding = self.get_embeddings([query])[0]
        
        # Search in ChromaDB
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k
        )
        
        # Format results
        formatted_results = []
        for i in range(len(results['documents'][0])):
            formatted_results.append({
                'text': results['documents'][0][i],
                'metadata': results['metadatas'][0][i],
                'distance': results['distances'][0][i]
            })
        
        return formatted_results

    def get_relevant_context(self, query: str, max_tokens: int = 2000) -> str:
        """Get relevant context for a query, managing context window."""
        results = self.similarity_search(query, k=5)
        
        # Sort by relevance score
        results.sort(key=lambda x: x['distance'])
        
        # Build context string
        context = ""
        current_tokens = 0
        
        for result in results:
            # Rough token estimation (1 token ≈ 4 chars)
            tokens = len(result['text']) // 4
            if current_tokens + tokens > max_tokens:
                break
                
            context += f"\nSource: {result['metadata']['source']}\n"
            context += f"{result['text']}\n"
            current_tokens += tokens
            
        return context.strip()
