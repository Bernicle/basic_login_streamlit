import streamlit as st
import bcrypt
from src.service.db_manager import get_user_by_username
from typing import Optional

def authenticate_user(username: str, password: str) -> bool:
    """
    Authenticates a user against the database and sets the Streamlit session state.
    
    Returns:
        bool: True if authentication succeeded, False otherwise.
    """
    # 1. Fetch user from DB
    user = get_user_by_username(username)

    if user:
        # 2. Securely verify password using bcrypt
        # bcrypt.checkpw automatically handles salting and hashing checks.
        # It takes bytes, so we encode the submitted password.
        if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password.encode('utf-8')):
            
            # 3. Authentication Success: Set secure session state
            st.session_state["authenticated"] = True
            st.session_state["username"] = user.username
            st.session_state["name"] = user.name
            st.session_state["user_id"] = user.id
            
            return True
        else:
            # Password mismatch
            st.session_state["authenticated"] = False
            return False
    else:
        # User not found
        st.session_state["authenticated"] = False
        return False

def logout():
    """Clears the session state to log the user out."""
    if st.session_state.get("authenticated"):
        del st.session_state["authenticated"]
        if "username" in st.session_state: del st.session_state["username"]
        if "name" in st.session_state: del st.session_state["name"]
        if "user_id" in st.session_state: del st.session_state["user_id"]
        # Streamlit rerun is needed to redraw the UI to the login screen
        st.experimental_rerun()
