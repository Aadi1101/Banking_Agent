import os
import chromadb
from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from dotenv import load_dotenv
from src.logger import logging
from src.utils.config import get_config

load_dotenv()  # Load environment variables if needed

persist_directory = get_config("PERSIST_DIRECTORY")
document_path = get_config("DOCUMENT_PATH")
collection_name = get_config("COLLECTION_NAME")

def initialize_vector_store(persist_directory=persist_directory, document_path=document_path,collection_name=collection_name):
    """Initialize Chroma vector store with Ollama embeddings and load documents if provided."""
    try:
        base_url = get_config("OLLAMA_HOST")
        logging.info("🔹 Initializing Ollama Embeddings...")
        embeddings_model = OllamaEmbeddings(model="nomic-embed-text",base_url=base_url)
        logging.info("✅ Ollama Embeddings Loaded.")

        # Initialize persistent ChromaDB client
        client = chromadb.PersistentClient(path=persist_directory)

        # Check if the collection exists
        existing_collections = [col.name for col in client.list_collections()]
        if collection_name in existing_collections:
            collection = client.get_collection(collection_name)
            logging.info("✅ Existing collection reinitialized.")
        else:
            collection = client.create_collection(name=collection_name)
            logging.info("✅ New collection created.")

        if document_path:
            logging.info(f"🔹 Loading document: {document_path}")
            loader = PyPDFLoader(document_path) if document_path.endswith(".pdf") else TextLoader(document_path)
            documents = loader.load()
            logging.info(f"✅ Documents loaded: {len(documents)}")  # Add this line

            text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
            doc_splits = text_splitter.split_documents(documents)
            logging.info(f"✅ Document splits created: {len(doc_splits)}") #add this line.
            texts = [chunk.page_content for chunk in doc_splits]
            embeddings = embeddings_model.embed_documents(texts)
            logging.info(f"✅ Embeddings created: {len(embeddings)}") #add this line.

            logging.info(f"✅ Adding {len(doc_splits)} text chunks to ChromaDB...")
            for idx, chunk in enumerate(doc_splits):
                collection.add(
                    documents=[chunk.page_content],
                    metadatas=[{'id': idx}],
                    embeddings=[embeddings[idx]],
                    ids=[str(idx)]
                )
            logging.info("✅ Document chunk added to chromadb") #add this line.
            logging.info(Chroma(persist_directory=persist_directory, embedding_function=embeddings_model))
            vectordb = Chroma(collection_name=collection_name, client=client, embedding_function=embeddings_model)
        else:
            logging.info("⚠️ No document provided. Initializing empty ChromaDB.")
            logging.info(Chroma(persist_directory=persist_directory, embedding_function=embeddings_model))
            vectordb = Chroma(persist_directory=persist_directory, embedding_function=embeddings_model)

        logging.info(f"✅ ChromaDB Initialized Successfully! Total Documents: {collection.count()}")
        logging.info("VECTOR DB: ",vectordb.get())
        return vectordb

    except Exception as e:
        logging.info(f"❌ Error initializing ChromaDB: {e}")
        return None

def get_retriever_from_vector_store(vectordb):
    """Retrieves data from ChromaDB."""
    try:
        if not vectordb:
            logging.info("❌ Vector store is not initialized. Cannot retrieve data.")
            return None

        logging.info("🔹 Creating Retriever from ChromaDB...")
        retriever = vectordb.as_retriever()
        logging.info("✅ Retriever is ready to use!")
        return retriever

    except Exception as e:
        logging.info(f"❌ Error retrieving data: {e}")
        return None

def add_documents_to_vector_store(vectordb, document_path):
    """Adds a new document to the vector database."""
    try:
        if not vectordb:
            logging.info("❌ Error: Vector store not initialized.")
            return False

        logging.info(f"🔹 Loading new document: {document_path}")
        loader = PyPDFLoader(document_path) if document_path.endswith(".pdf") else TextLoader(document_path)
        documents = loader.load()

        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        doc_splits = text_splitter.split_documents(documents)

        logging.info(f"✅ Adding {len(doc_splits)} text chunks to ChromaDB...")
        vectordb.add_documents(doc_splits)  # Add directly to the existing DB
        logging.info(f"✅ Document added successfully! Total Documents: {vectordb._collection.count()}")
        return True

    except Exception as e:
        logging.info(f"❌ Error adding document to ChromaDB: {e}")
        return False
