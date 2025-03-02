from langchain.chains import RetrievalQA
from src.utils.llm_manager import get_ollama_llm

def retrieve_from_documents(retriever, query):
    """Retrieves information from documents using the provided retriever."""
    if retriever:
        qa_chain = RetrievalQA.from_chain_type(
            llm=get_ollama_llm(),  # Or whichever LLM you want to use for retrieval
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True, # Return source documents for context
        )
        try:
            result = qa_chain({"query": query})
            return result["result"]
        except Exception as e:
            return f"Error during document retrieval: {e}"
    else:
        return "Retriever not available."