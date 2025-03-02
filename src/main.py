import streamlit as st
from src.ui.chat_interface import display_chat_interface
from src.components.agent import Agent
from src.utils.database import get_user_id_by_username #Import this function.
from src.utils.config import get_config
from src.logger import logging

def main():

    if not get_config("DB_HOST") or not get_config("DB_USER") or not get_config("DB_PASSWORD") or not get_config("DB_NAME"):
        st.error("Database configuration is missing in .env file.")
        return

    # Dummy user ID for now (replace with actual user ID later)
    # Or any other default user ID

    if "agent" not in st.session_state:
        st.session_state.user_id = 1
        st.session_state.agent = Agent()
        

    display_chat_interface(st.session_state.agent)

if __name__ == "__main__":
    logging.info("Starting to run the Application.")
    main()