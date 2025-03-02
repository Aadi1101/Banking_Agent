from src.utils.web_search_client import search_web

def perform_web_search(query):
    """Performs a web search using the web_search_client."""
    try:
        results = search_web(query)
        return results if results else "No web search results found."
    except Exception as e:
        return f"Error during web search: {e}"