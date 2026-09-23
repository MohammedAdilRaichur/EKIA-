import os
import sys

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

from app.rag.ingestion import process_documents, get_text_chunks
from app.rag.vectorstore import ingest_to_vectorstore

if __name__ == "__main__":
    docs_dir = os.path.join(base_dir, "data", "documents")
    print("Extracting text from PDFs...")
    docs = process_documents(docs_dir)
    print("Chunking documents...")
    chunks, metadatas = get_text_chunks(docs)
    print("Embedding and storing in Chroma...")
    ingest_to_vectorstore(chunks, metadatas)
    print("Done!")
