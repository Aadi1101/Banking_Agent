import streamlit as st
import os
from src.components.agent import Agent  # Import the Agent class

def display_chat_interface(agent): #Pass agent object to the display function.
    """Displays the chat interface and handles user interactions."""

    st.title("Banking AI Chatbot")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for chat in st.session_state.chat_history:
        with st.chat_message(chat["role"]):
            st.write(chat["content"])

    user_query = st.chat_input("Ask me anything about your bank!")

    if user_query:
        with st.chat_message("user"):
            st.write(user_query)

        with st.spinner("Thinking..."):  # Add a spinner to indicate processing
            response = agent.run(user_query, "user_id_placeholder")  # Replace with actual user ID
            with st.chat_message("assistant"):
                st.write(response)

        st.session_state.chat_history.append({"role": "user", "content": user_query})
        st.session_state.chat_history.append({"role": "assistant", "content": response})

    # Goal Setting
    goal = st.text_input("Set a goal:")
    if goal:
        agent.set_goal("user_id_placeholder", goal)  # Replace with actual user ID
        st.write("Goal set!")

    # Goal Status
    if st.button("Check Goal Status"):
        status = agent.get_goal_status("user_id_placeholder")  # Replace with actual user ID
        if status:
            st.write(f"Goal: {status['goal']}")
            st.write(f"Progress: {status['progress']}")
        else:
            st.write("No goal set.")

    # Memory Retrieval
    memory_query = st.text_input("Retrieve memory (query):")
    if memory_query:
        memories = agent.get_memory(memory_query)
        st.write("Retrieved Memories:")
        for memory in memories:
            st.write(memory.page_content)

    #Clear memory.
    if st.button("Clear Memory"):
        agent.clear_memory()
        st.write("Memory cleared.")

    # Add Document
    uploaded_file = st.file_uploader("Upload a document", type=["txt", "pdf"])
    if uploaded_file is not None:
        with open(uploaded_file.name, "wb") as f:
            f.write(uploaded_file.getbuffer())
        if agent.add_document(uploaded_file.name):
            st.success("Document added successfully!")
        else:
            st.error("Failed to add document.")
        os.remove(uploaded_file.name) #Delete file after upload.