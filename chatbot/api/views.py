from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.conf import settings
import openai
from dotenv import load_dotenv
import os
from pathlib import Path
from vector_store.vector_store import VectorStore
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = openai.OpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
    base_url=os.getenv('GITHUB_API_URL')
)

# Initialize vector store with insurance PDFs
base_dir = Path(__file__).resolve().parent.parent.parent
docs_dir = base_dir / 'insurance_files'
vector_store = VectorStore(persist_directory=str(base_dir / "chroma_db"))

# Process insurance PDFs if they haven't been processed yet
if not os.path.exists(str(base_dir / "chroma_db")):
    try:
        from vector_store.document_loader import process_document
        from vector_store.process_documents import process_documents_directory
        logger.info("Processing insurance documents...")
        documents = process_documents_directory(str(docs_dir))
        vector_store.add_documents(documents)
        logger.info(f"Successfully processed and added {len(documents)} document chunks to vector store")
    except Exception as e:
        logger.error(f"Error processing documents: {str(e)}")
        raise

@api_view(['POST'])
def ask_question(request):    
    try:
        # Get question from request
        question = request.data.get('question')
        if not question:
            return Response({'error': 'Question is required'}, status=400)

        # Get relevant context from vector store using OpenAI embeddings
        try:
            context = vector_store.get_relevant_context(question)
            logger.info(f"Found context for question: {question[:50]}...")
        except Exception as e:
            logger.error(f"Error getting context: {str(e)}")
            context = ""

        # If no context found, return "I Don't know"
        if not context:
            return Response({'answer': "I Don't know"})

        # Call OpenAI API with context
        response = client.chat.completions.create(
            model="openai/gpt-4.1",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that answers insurance-related questions. Only use the provided context to answer questions. If you cannot find the answer in the context, say 'I Don't know'."},
                {"role": "user", "content": f"Context: {context}\n\nQuestion: {question}"}
            ],
            temperature=0.7,
            max_tokens=500
        )

        # Extract the answer from OpenAI response
        answer = response.choices[0].message.content
        
        # If no relevant information found
        if "I don't have enough information" in answer.lower() or "I cannot answer" in answer.lower():
            return Response({'answer': "I Don't know"})

        return Response({'answer': answer})

    except Exception as e:
        print("Received request:", e)  # Debugging line
        return Response({'error': str(e)}, status=500)
