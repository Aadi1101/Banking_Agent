import os
from dotenv import load_dotenv
from langchain.llms import Ollama, Gemini

load_dotenv()  # Load environment variables

def get_ollama_llm(system_prompt=None):
    """Initializes and returns an Ollama LLM."""
    model_name = os.getenv("OLLAMA_MODEL_NAME")
    if not model_name:
        raise ValueError("OLLAMA_MODEL_NAME environment variable not set.")
    try:
        if system_prompt:
            return Ollama(model=model_name, system=system_prompt)
        else:
            return Ollama(model=model_name)
    except Exception as e:
        print(f"Error initializing Ollama: {e}")
        return None  # Or handle the error as needed

def get_gemini_llm(system_prompt=None):
    """Initializes and returns a Gemini LLM."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        # Handle the case where the API key is not set.
        # Options: raise an exception, return None, use a default key, etc.
        # Here, we raise a ValueError to make it explicit.
        raise ValueError("GEMINI_API_KEY environment variable not set.")
    try:
        if system_prompt:
            return Gemini(api_key=api_key, system=system_prompt)
        else:
            return Gemini(api_key=api_key)
    except Exception as e:
        print(f"Error initializing Gemini: {e}")
        return None  # Or handle the error as needed

# Example usage (in other modules):
# ollama_llm = get_ollama_llm(system_prompt="You are a helpful banking assistant.")
# gemini_llm = get_gemini_llm()