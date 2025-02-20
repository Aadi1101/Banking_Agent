from langchain.agents import Tool
from langchain.chains import RetrievalQA
from src.utils.web_search_utils import search_web
from src.utils.bank_api import BankAPI # Import the bank API.

def create_tools(retriever, ollama_llm, gemini_llm):
    """Creates and returns a list of LangChain tools."""

    bank_api = BankAPI() # Initialize the bank API.

    retriever_qa = RetrievalQA.from_chain_type(
        llm=ollama_llm, chain_type="stuff", retriever=retriever,
        return_source_documents=True #Return source documents.
    )

    tools = [
        Tool(
            name="Document_Retrieval",
            func=retriever_qa.run,
            description="Useful for retrieving information from the bank's documents.  Use this tool when the user asks a question about the bank's policies, products, or services.",
        ),
        Tool(
            name="General_Conversation",
            func=ollama_llm.invoke,
            description="Useful for general conversation, casual greetings, and small talk.  Use this tool when the user's query is not related to specific bank information or tasks.",
        ),
        Tool(
            name="Financial_Analysis",
            func=gemini_llm.invoke,
            description="Useful for complex financial calculations, analysis, and reasoning.  Use this tool when the user asks a financial question or requests a financial analysis.",
        ),
        Tool(
            name="Web_Search",
            func=search_web,
            description="Useful for searching the web for information not available in the bank's documents.  Use this tool when the user asks a question that requires external knowledge or information.",
        ),
        Tool(
            name="Check_Balance",
            func=bank_api.check_balance,
            description="Useful for checking the user's account balance. Use this tool when the user asks to see their balance.",
        ),
        Tool(
            name="Transfer_Funds",
            func=bank_api.transfer_funds,
            description="Useful for transferring funds between accounts.  Use this tool when the user wants to make a transfer.",
        ),
    ]
    return tools