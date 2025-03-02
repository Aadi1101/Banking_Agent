import requests
import chromadb
from langchain_community.embeddings import OllamaEmbeddings
from langchain_chroma import Chroma
from src.utils.llm_manager import get_ollama_llm
from src.utils.vector_db_manager import initialize_vector_store
from src.logger import logging
from src.utils.config import get_config

class Memory:
    def __init__(self):
        """Initializes memory using a separate ChromaDB collection ('memory-store')."""
        try:
            logging.info("🔹 Checking Ollama server availability...")
            if not self._is_ollama_running():
                raise RuntimeError("❌ Ollama server is not running")

            logging.info("🔹 Initializing Memory Store Collection ('memory-store')...")
            self.memory_store = initialize_vector_store(persist_directory="db", collection_name="memory-store")
            if not self.memory_store:
                raise RuntimeError("❌ Failed to initialize memory store.")

            logging.info("✅ Memory store initialized successfully.")

        except Exception as e:
            logging.info(f"❌ Error initializing memory store: {e}")
            self.memory_store = None  # Prevent crashes if initialization fails

    def _is_ollama_running(self):
        """Checks if Ollama is running."""
        try:
            base_url = get_config("OLLAMA_HOST")
            response = requests.get(base_url)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False

    def add_memory(self, text):
        """Adds text to memory store ('memory-store' collection)."""
        try:
            if not self.memory_store:
                logging.info("⚠️ Memory store is not initialized.")
                return False

            if not text.strip():
                logging.info("⚠️ Warning: Cannot add empty text to memory.")
                return False

            self.memory_store.add_texts([text])
            logging.info(f"✅ Memory added: {text[:50]}...")
            return True

        except Exception as e:
            logging.info(f"❌ Error adding memory: {e}")
            return False

    def retrieve_memory(self, query):
        """Retrieves similar memory chunks from 'memory-store'."""
        try:
            if not self.memory_store:
                logging.info("⚠️ Memory store is not initialized.")
                return []

            if not query.strip():
                logging.info("⚠️ Warning: Empty query provided for memory retrieval.")
                return []

            retriever = self.memory_store.as_retriever()
            results = retriever.get_relevant_documents(query)

            if results:
                logging.info(f"✅ Retrieved {len(results)} relevant memory chunks.")
            else:
                logging.info("ℹ️ No relevant memory found.")
            return [doc.page_content for doc in results]

        except Exception as e:
            logging.info(f"❌ Error retrieving memory: {e}")
            return []

    def summarize_memory(self):
        """Summarizes stored memory using an LLM and updates the 'memory-store' collection."""
        try:
            if not self.memory_store:
                logging.info("⚠️ Memory store is not initialized.")
                return None

            retriever = self.memory_store.as_retriever()
            all_memories = retriever.get_relevant_documents("")

            if not all_memories:
                logging.info("ℹ️ No memory to summarize.")
                return None

            text_to_summarize = " ".join([doc.page_content for doc in all_memories])

            logging.info("🔹 Summarizing memory using Ollama LLM...")
            summarizer_llm = get_ollama_llm(system_prompt="You are a memory summarizer. Summarize the provided text.")
            summary = summarizer_llm.invoke(text_to_summarize)

            # Clear the memory store and store the summarized text
            self.clear_memory()
            self.add_memory(summary)

            logging.info(f"✅ Memory summarized: {summary[:50]}...")
            return summary

        except Exception as e:
            logging.info(f"❌ Error summarizing memory: {e}")
            return None

    def clear_memory(self):
        """Clears all stored memory in the 'memory-store' collection while keeping the collection itself."""
        try:
            if not self.memory_store:
                logging.info("⚠️ Memory store is not initialized.")
                return

            # Retrieve all document IDs and delete them
            all_docs = self.memory_store._collection.get()  # Get all documents
            doc_ids = all_docs["ids"] if "ids" in all_docs else []

            if doc_ids:
                self.memory_store._collection.delete(ids=doc_ids)
                logging.info(f"✅ Cleared {len(doc_ids)} memory records while keeping the 'memory-store' collection.")
            else:
                logging.info("ℹ️ No memory records to clear.")

        except Exception as e:
            logging.info(f"❌ Error clearing memory: {e}")
