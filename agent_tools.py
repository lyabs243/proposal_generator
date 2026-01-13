import os
from typing import List, Optional
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from app_utils import generate_key
from agents import Agent, FunctionTool, RunContextWrapper, function_tool

load_dotenv(override=True)

@function_tool 
async def search_vector_db(query: str, k: int = 3, categories: Optional[List[str]] = None) -> str:
    """
    Search in the vector database for relevant documents based on the query.
    
    Args:
        query (str): The search query text.
        k (int): Number of results to return. Defaults to 3.
        categories (Optional[List[str]]): List of categories to filter by. 
                                          If multiple categories are provided, matches any (OR logic).
    """
    # Use absolute path for the database directory based on the file location
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_name = os.path.join(current_dir, "chroma_db")
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    
    # Initialize the vector store
    vectordb = Chroma(
        collection_name="freelance_data",
        embedding_function=embeddings,
        persist_directory=db_name,
    )
    
    # Construct the filter
    filter_dict = None
    if categories:
        if len(categories) == 1:
            key = generate_key(categories[0])
            filter_dict = {key: True}
        else:
            filter_dict = {"$or": [{generate_key(c): True} for c in categories]}
            
    # Perform the search
    results = vectordb.similarity_search(query, k=k, filter=filter_dict)
    
    # Format the results
    formatted_results = []
    for doc in results:
        metadata_str = ", ".join(f"{k}: {v}" for k, v in doc.metadata.items())
        formatted_results.append(f"Metadata: {metadata_str}\nContent:\n{doc.page_content}")
        
    return "\n\n---\n\n".join(formatted_results)
