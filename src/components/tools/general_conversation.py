from src.utils.llm_manager import get_ollama_llm
from src.utils.config import get_config

def have_general_conversation(query):
    """Engages in general conversation using the Ollama LLM."""
    general_conversation_prompt = get_config("GENERAL_CONVERSATION_PROMPT")
    ollama_llm = get_ollama_llm(system_prompt=general_conversation_prompt)
    if ollama_llm:
        try:
            return ollama_llm(query)
        except Exception as e:
            return f"Error during general conversation: {e}"
    else:
        return "Ollama LLM not available."