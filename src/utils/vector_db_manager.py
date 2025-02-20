import os
from dotenv import load_dotenv
from langchain.embeddings import GeminiEmbeddings, OllamaEmbeddings  # Import both
from langchain.vectorstores import Chroma
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter

load_dotenv()

def initialize_vector_store(embeddings_model=None, persist_directory=None):
    """Initializes and returns a ChromaDB vector store. Uses Gemini embeddings if available, falls back to Ollama."""

    if embeddings_model is None:
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            try:
                embeddings_model = GeminiEmbeddings()
                print("Using Gemini embeddings.")
            except Exception as e:  # Catch potential Gemini initialization errors
                print(f"Error initializing Gemini embeddings: {e}. Falling back to Ollama.")
                embeddings_model = OllamaEmbeddings() # Fallback to Ollama
        else:
            print("Gemini API key not found. Using Ollama embeddings.")
            embeddings_model = OllamaEmbeddings()

    if persist_directory is None:
        persist_directory = "db"

    try:
        vectordb = Chroma(persist_directory=persist_directory, embedding_function=embeddings_model)
        return vectordb
    except Exception as e:
        print(f"Error initializing ChromaDB: {e}")
        return None

def add_documents_to_vector_store(vectordb, document_path):
    """Adds documents from a file to the vector store."""
    try:
        loader = TextLoader(document_path)
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        texts = text_splitter.split_documents(documents)
        vectordb.add_documents(texts)
        return True
    except Exception as e:
        print(f"Error adding documents to ChromaDB: {e}")
        return False

def get_retriever_from_vector_store(vectordb):
    """Gets a retriever object from the vector store."""
    if vectordb:
        return vectordb.as_retriever()
    return None

# Example usage (in other modules):
# vectordb = initialize_vector_store()  # Will automatically choose embeddings
# if vectordb:
#     add_documents_to_vector_store(vectordb, os.getenv("DOCUMENT_PATH"))
#     retriever = get_retriever_from_vector_store(vectordb)
#     if retriever:
#         results = retriever.search("What are the interest rates for personal loans?")
#         print(results)