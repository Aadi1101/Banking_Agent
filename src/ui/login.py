import streamlit as st
from src.utils.auth_manager import create_authenticator  

def display_login(credentials):  
    """Displays the login/signup interface using Streamlit and streamlit_authenticator."""

    authenticator = create_authenticator(credentials)  

    # Ensure session state keys exist before accessing them
    auth_status = st.session_state.get("authentication_status", None)  
    user_name = st.session_state.get("name", "")

    if auth_status:  # User is authenticated
        st.sidebar.success(f"Logged in as {user_name}")
        authenticator.logout("Logout", "sidebar")  # Logout button in sidebar

    elif auth_status is False:  # Invalid login
        st.sidebar.error("Invalid Username or Password")
    
    else:  # Default case: Show login form
        st.sidebar.warning("Please enter your credentials")
        authenticator.login("Login", "sidebar")  # Ensure the login form is shown
