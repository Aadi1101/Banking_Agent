import streamlit as st
from src.components.agent import Agent
from src.utils.config import get_config
from src.utils.database import db_connection, fetch_user_balance
import os
from dotenv import load_dotenv
from src.logger import logging
from src.utils.config import get_config
load_dotenv()

def display_chat_interface(agent):
    """Displays the banking chatbot interface in Streamlit."""

    st.title("💬 Banking Chatbot")

    # Initialize user session state
    st.session_state.setdefault("messages", [])

    # Set user_id to 1
    if "user_id" not in st.session_state:
        st.session_state["user_id"] = 1

    # Add description and example queries before welcome message
    if not st.session_state.messages:
        description_message = get_config("DESCRIPTION_MESSAGE")
        st.session_state.messages.append({"role": "assistant", "content": description_message})

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input
    if user_input := st.chat_input("Your message"):

        # Clear memory command
        if user_input.lower() == "clear memory":
            agent.clear_memory()
            st.session_state.messages = []
            st.success("Memory cleared successfully! 🔄")
            st.experimental_rerun()
            return

        # Add document command
        if user_input.lower().startswith("add document"):
            parts = user_input.split(" ", 2)
            if len(parts) < 3:
                st.error("❌ Invalid command. Usage: `add document <filename>`")
            else:
                filename = parts[2].strip()
                if filename:
                    success = agent.add_document(filename)
                    if success:
                        st.success(f"✅ Document '{filename}' added successfully!")
                    else:
                        st.error(f"❌ Failed to add document. Ensure the file exists and is accessible.")
                else:
                    st.error("❌ Please provide a valid filename.")
            return

        # Get memory command
        if user_input.lower().startswith("get memory"):
            parts = user_input.split(" ", 2)
            if len(parts) < 3:
                st.error("❌ Invalid command. Usage: `get memory <query>`")
            else:
                query = parts[2].strip()
                memory = agent.get_memory(query)
                if memory:
                    st.write("📜 Retrieved Memory:")
                    st.write(memory)
                else:
                    st.warning("⚠️ No matching memory found.")
            return

        # Store user message in session
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Agent response
        with st.chat_message("assistant"):
            with st.spinner("Processing..."):
                logging.info("Processing Agent Response")
                agent_response = agent.run(user_input, st.session_state["user_id"])
                st.markdown(agent_response)

        # Store agent response in session
        logging.info("Stored Agent Response")
        st.session_state.messages.append({"role": "assistant", "content": agent_response})