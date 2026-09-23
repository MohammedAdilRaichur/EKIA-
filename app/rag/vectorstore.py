import os
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from app.config import config

def get_vectorstore():
    # Initialize embeddings
    embeddings = HuggingFaceEmbeddings(model_name=config.EMBEDDING_MODEL)
    
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    persist_directory = os.path.join(base_dir, "data", "vectorstore")
    
    vectorstore = Chroma(
        collection_name="enterprise_knowledge",
        embedding_function=embeddings,
        persist_directory=persist_directory
    )
    return vectorstore

def ingest_to_vectorstore(chunks, metadatas):
    vectorstore = get_vectorstore()
    vectorstore.add_texts(texts=chunks, metadatas=metadatas)
    print(f"Ingested {len(chunks)} chunks into vector store.")
