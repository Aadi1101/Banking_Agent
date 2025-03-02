from src.utils.llm_manager import get_gemini_llm

def perform_advanced_reasoning(query):
    """Performs advanced reasoning using the Gemini LLM."""
    gemini_llm = get_gemini_llm(system_prompt="You are a skilled financial analyst adept at advanced reasoning.")
    if gemini_llm:
        try:
            return gemini_llm(query)
        except Exception as e:
            return f"Error during advanced reasoning: {e}"
    else:
        return "Gemini LLM not available."