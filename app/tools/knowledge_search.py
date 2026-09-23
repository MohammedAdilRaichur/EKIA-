from langchain.tools import tool
from app.rag.vectorstore import get_vectorstore
from app.config import config
import json

@tool
def knowledge_search(query: str, filters: str = None) -> str:
    """
    Search the enterprise knowledge base for policies, guidelines, and company information.
    Use this tool when answering questions about company rules, IT guides, or handbooks.
    
    Args:
        query (str): The search query to look for in the knowledge base.
        filters (str, optional): A JSON string representing metadata filters, e.g. '{"department": "HR"}'.
    """
    vectorstore = get_vectorstore()
    
    search_kwargs = {"k": config.TOP_K}
    if filters:
        try:
            filter_dict = json.loads(filters)
            search_kwargs["filter"] = filter_dict
        except Exception:
            pass
            
    results = vectorstore.similarity_search(query, **search_kwargs)
    
    if not results:
        return "No relevant information found in the knowledge base."
        
    formatted_results = []
    for doc in results:
        metadata = doc.metadata
        source = f"Source: {metadata.get('document_name', 'Unknown')}"
        formatted_results.append(f"{source}\n{doc.page_content}")
        
    return "\n\n---\n\n".join(formatted_results)
