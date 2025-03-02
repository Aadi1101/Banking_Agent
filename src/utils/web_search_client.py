from googlesearch import search

def search_web(query, num_results=5):
    """Searches Google using the `googlesearch-python` package (No API needed) and returns results as a string."""
    try:
        results = list(search(query, num_results=num_results))
        return "\n".join(results) if results else "No relevant web search results found."
    except Exception as e:
        return f"Error during web search: {e}"
