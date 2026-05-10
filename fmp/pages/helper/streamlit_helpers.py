import streamlit as st


def require_login():
    """Redirect to home if user is not logged in."""
    if not st.session_state.get("login_status", False):
        st.warning("Please login first from the Home page.")
        st.stop()
