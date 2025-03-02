from langchain.agents import Tool
from src.components.tools.advanced_reasoning import perform_advanced_reasoning
from src.components.tools.document_retrieval import retrieve_from_documents
from src.components.tools.general_conversation import have_general_conversation
from src.components.tools.web_search import perform_web_search
from src.utils.bank_api import BankAPI
import streamlit as st
from src.logger import logging
from src.utils.config import get_config

def create_tools(retriever, ollama_llm, gemini_llm, user_id=None):
    """Creates and returns a list of LangChain tools, including Financial Analysis."""

    bank_api = BankAPI()
    document_retrieval_prompt = get_config("DOCUMENT_RETRIEVAL_TOOL_DESCRIPTION")
    general_conversation_prompt = get_config("GENERAL_CONVERSATION_TOOL_DESCRIPTION")
    financial_analysis_prompt = get_config("FINANCIAL_ANALYSIS_TOOL_DESCRIPTION")
    web_search_prompt = get_config("WEB_SEARCH_TOOL_DESCRIPTION")
    check_balance_prompt = get_config("CHECK_BALANCE_TOOL_DESCRIPTION")
    user_details_prompt = get_config("USER_DETAILS_TOOL_DESCRIPTION")
    transaction_prompt = get_config("TRANSACTION_TOOL_DESCRIPTION")
    savings_balance_prompt = get_config("SAVINGS_BALANCE_TOOL_DESCRIPTION")
    loans_prompt = get_config("LOANS_TOOL_DESCRIPTION")
    investments_prompt = get_config("INVESTMENTS_TOOL_DESCRIPTION")
    donations_prompt = get_config("DONATION_TOOL_DESCRIPTION")
    blocked_prompt = get_config("BLOCKED_ACCOUNT_DESCRIPTION")

    tools = [
        Tool(
            name="Document_Retrieval",
            func=lambda query: retrieve_from_documents(retriever, query),
            description=document_retrieval_prompt,
        ),
        Tool(
            name="General_Conversation",
            func=have_general_conversation,
            description=general_conversation_prompt,
        ),
        Tool(
            name="Financial_Analysis",
            func=perform_advanced_reasoning,
            description=financial_analysis_prompt,
        ),
        Tool(
            name="Web_Search",
            func=perform_web_search,
            description=web_search_prompt,
        ),
        Tool(
            name="Check_Balance",
            func=bank_api.check_balance,
            description=check_balance_prompt,
        ),
        Tool(
            name="Get_User_Details",
            func=bank_api.get_user_details,
            description=user_details_prompt,
        ),
        Tool(
            name="Get_Transactions",
            func=bank_api.get_transactions,
            description=transaction_prompt,
        ),
        Tool(
            name="Get_Savings_Balance",
            func=bank_api.get_savings_balance,
            description=savings_balance_prompt,
        ),
        Tool(
            name="Get_Loans",
            func=bank_api.get_loans,
            description=loans_prompt,
        ),
        Tool(
            name="Get_Investments",
            func=bank_api.get_investments,
            description=investments_prompt,
        ),
        Tool(
            name="Get_Donations",
            func=bank_api.get_donations,
            description=donations_prompt,
        ),
        Tool(
            name="Is_Account_Blocked",
            func=bank_api.is_blocked,
            description=blocked_prompt,
        ),
    ]
    logging.info("Chose the tool to used: ",tools)
    return tools