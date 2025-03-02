import streamlit as st
from streamlit_authenticator import Authenticate
from src.utils.config import get_config

def create_authenticator(credentials):
    """Creates and returns a Streamlit authenticator object, ensuring it's created only once."""
    
    if "authenticator" not in st.session_state:
        st.session_state.authenticator = Authenticate(
            credentials,
            get_config("COOKIE_NAME"),
            get_config("COOKIE_KEY"),
            get_config("COOKIE_EXPIRY_DAYS"),
            st.session_state
        )

    return st.session_state.authenticator
