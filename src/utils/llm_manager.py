import os
import google.generativeai as genai
from langchain.llms import Ollama
from src.utils.config import get_config
from src.logger import logging

def get_ollama_llm(system_prompt=None):
    """Initializes and returns an Ollama LLM instance."""
    model_name = get_config("OLLAMA_MODEL_NAME")  # Get model name from config
    base_url = get_config("OLLAMA_HOST")
    logging.info(model_name)

    if not model_name or model_name== "":
        raise ValueError("OLLAMA_MODEL_NAME is missing or empty.")

    try:
        return Ollama(model="mistral", system=system_prompt,base_url=base_url)
    except Exception as e:
        raise RuntimeError(f"Error initializing Ollama: {e}") from e

def get_gemini_llm(system_prompt=None):
    """Initializes and returns a Gemini LLM instance using google.generativeai."""
    api_key = get_config("GEMINI_API_KEY")
    gemini_model = get_config("GEMINI_MODEL_NAME")

    if not api_key or api_key.strip() == "":
        raise ValueError("GEMINI_API_KEY is missing or empty.")

    # Configure the API key properly
    genai.configure(api_key=api_key)

    try:
        model = genai.GenerativeModel(gemini_model)  # Initialize the model

        def _gemini_llm(prompt):
            """Internal function to call Gemini."""

            if system_prompt:
                prompt = f"{system_prompt}\n{prompt}"

            response = model.generate_content(prompt)
            
            # Handle response correctly
            return response.text if hasattr(response, 'text') else response

        return _gemini_llm  # Return the callable function

    except Exception as e:
        raise RuntimeError(f"Error initializing or using Gemini: {e}") from e
