from django.core.management.base import BaseCommand
from pathlib import Path
from vector_store import initialize_vector_store

class Command(BaseCommand):
    help = 'Initialize vector store with documents from Insurance PDFs folder'

    def handle(self, *args, **options):
        try:
            # Get the path to Insurance PDFs folder
            base_dir = Path(__file__).resolve().parent.parent.parent.parent.parent
            docs_dir = base_dir / 'Insurance PDFs'
            print(f'Base directory: {base_dir} {docs_dir}')
            
            if not docs_dir.exists():
                self.stdout.write(self.style.ERROR(f'Directory not found: {docs_dir}'))
                return

            self.stdout.write(self.style.SUCCESS(f'Processing documents from: {docs_dir}'))
            
            # Initialize vector store
            vector_store = initialize_vector_store(str(docs_dir))
            
            self.stdout.write(self.style.SUCCESS('Vector store initialized successfully!'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error initializing vector store: {str(e)}'))
