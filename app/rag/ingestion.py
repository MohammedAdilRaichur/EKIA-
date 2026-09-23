import os
import pymupdf
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.config import config

def extract_text_and_metadata(pdf_path):
    doc = pymupdf.open(pdf_path)
    
    filename = os.path.basename(pdf_path)
    department = os.path.basename(os.path.dirname(pdf_path))
    
    full_text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        full_text += page.get_text("text") + "\n"
        
    return {
        "text": full_text,
        "metadata": {
            "document_name": filename,
            "department": department,
            "source_path": pdf_path,
            "access_level": "Employee" # default
        }
    }

def process_documents(docs_dir):
    documents = []
    for root, _, files in os.walk(docs_dir):
        for file in files:
            if file.endswith('.pdf'):
                path = os.path.join(root, file)
                documents.append(extract_text_and_metadata(path))
    return documents

def get_text_chunks(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP,
        separators=["\n\n", "\n", " ", ""]
    )
    
    chunks = []
    metadatas = []
    for doc in documents:
        splits = text_splitter.split_text(doc["text"])
        chunks.extend(splits)
        metadatas.extend([doc["metadata"]] * len(splits))
        
    return chunks, metadatas
