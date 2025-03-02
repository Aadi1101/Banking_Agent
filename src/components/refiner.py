from src.utils.llm_manager import get_ollama_llm

def refine_response(response, user_query):
    refiner_llm = get_ollama_llm(system_prompt="""
    Refine the provided response to better answer the user's query.
    """)
    prompt = f"Original response: {response}\nUser query: {user_query}\nRefined response:"
    refined = refiner_llm.invoke(prompt)
    return refined