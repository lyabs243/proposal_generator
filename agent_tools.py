import os
from typing import List, Optional
from dotenv import load_dotenv
from langchain_openai import OpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from app_utils import generate_key
from agents import function_tool
from models.technology_choice import TechnologyChoice, TechnologyChoicesResponse

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

@function_tool
async def get_technologies(text: str) -> TechnologyChoicesResponse:
    """
    Extract and return a list of technologies mentioned in the input text.
    
    Args:
        text (str): The input text to analyze.
    Returns:
        TechnologyChoicesResponse: A list of TechnologyChoice objects with technology names and reasons.
    """
    from openai import OpenAI

    allowed_technologies = 'AI, API, Admob, Android, Audio, BLOC, Bluetooth, Bootstrap, CSS, Calendar, Chart, Chat, Chatbot, Chroma, Cloud Functions, Code Generation, CodeIgniter, Custom Paint, Dart, Drag and Drop, Email, Excel, FFMPEG, Facebook API, Firebase, Firestore, Flutter, Gemini, Google Analytics, Google Maps, Gradio, Groq, HTML, In App Purchase, JSON, Java, JavaScript, Jupyter, LangChain, Laravel, Live Score, Local Database, Lottie, Multi Platform, MySQL, NFC, Node.js, Notifications, Open Weather API, OpenAI, PDF Generation, PHP, Package, Poll, Project architecture, Python, QR Code, RAG, RSS, Recorder, Responsive, Rive, SQLite, Scrapy, Socket, Speech to Text, Telegram Bot, Timer, Translation, Twitter API, Unit Testing, Video, Video Generation, Vue JS, Web, Web Scrapping, WebView, Windows, WordPress, XML, Yandex API, iOS'

    client = OpenAI()
    response = client.responses.parse(
        model="gpt-4o-mini",
        input=[
            {
                "role": "system",
                "content": "Your goal is to extract technologies mentioned in the user's text. "
                "You can only return from the following list of technologies: " + allowed_technologies + ". Return them exactly as they appear in this list. "
                "If it has nothing to do with technologies, return an empty list. "
            },
            {"role": "user", "content": text},
        ],
        text_format= TechnologyChoicesResponse,
    )

    return response.output_parsed