import streamlit as st
import bcrypt
import uuid
from streamlit_cookies_controller import CookieController
from src.service.db_manager import get_user_by_username, get_user_by_token, set_user_session_token
from typing import Optional

from datetime import datetime, timedelta

# --- Configuration ---
COOKIE_NAME = "prod_session_id"
COOKIE_EXPIRY_DAYS = 7


# Initialize Cookie Controller outside functions to avoid repeated creation
try:
    # CookieController needs to be initialized only once per app run
    CONTROLLER = CookieController()
except Exception as e:
    # Fallback if the environment prevents cookie access.
    # The application will still function but persistence across refreshes will fail.
    print(f"WARNING: Could not initialize CookieController: {e}")
    CONTROLLER = None

def _set_session_state_logged_in(user):
    """Internal helper to set Streamlit session state and associated user details."""
    st.session_state["authenticated"] = True
    st.session_state["username"] = user.username
    st.session_state["name"] = user.name
    st.session_state["user_id"] = user.id


def check_cookie_authentication():
    """
    Checks the cookie for a valid, secure session token (UUID). 
    If verified against the database, it restores the Streamlit session state.
    This is the core mechanism for secure persistence across hard refreshes.
    """
    # 1. Skip if the user is already authenticated in the current run cycle
    if st.session_state.get("authenticated") is True:
        return
        
    if CONTROLLER:
        token = CONTROLLER.get(COOKIE_NAME)
        
        # 2. Check for a token
        if token and len(token) > 10: 
            # 3. Look up user by the token (SECURE server-side verification via DB)
            user = get_user_by_token(token)
            
            if user and user.session_token == token:
                # 4. Token verified: Restore full session state
                _set_session_state_logged_in(user)
                # st.info(f"Welcome back, {user.name} (Session Restored).")
                return
            
            # If token is invalid or no longer exists in DB, remove it from the client
            CONTROLLER.remove(COOKIE_NAME)
    
    # 5. Default state if no cookie or invalid cookie
    st.session_state["authenticated"] = False


def authenticate_user(username: str, password: str) -> bool:
    """
    Authenticates a user against the database and sets the Streamlit session state.
    
    Returns:
        bool: True if authentication succeeded, False otherwise.
    """
    user = get_user_by_username(username)

    if user:
        if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password.encode('utf-8')):
            
            # 1. Generate and save a secure token (UUID)
            secure_token = str(uuid.uuid4())
            # Uses set_user_session_token from db_manager.py to update the database
            if set_user_session_token(user.id, secure_token):
                
                # 2. Set the secure token in the client's browser cookie
                if CONTROLLER:

                    current_datetime = datetime.now()
                    future_datetime = current_datetime + timedelta(days=COOKIE_EXPIRY_DAYS)
                    CONTROLLER.set(COOKIE_NAME, secure_token, expires=future_datetime)
                
                # 3. Set Streamlit session state
                _set_session_state_logged_in(user)
                return True
            else:
                st.error("Authentication failed: Could not persist session token to DB.")
                return False
        return False
    else:
        return False

def logout():
    """Clears the session state and removes the persistent cookie."""
    if st.session_state.get("authenticated"):
        user_id = st.session_state.get("user_id")
        
        # 1. Clear the session token from the database (token=None)
        if user_id:
            set_user_session_token(user_id, None)

        # 2. Remove the persistent cookie from the client
        if CONTROLLER:
            CONTROLLER.remove(COOKIE_NAME)
        
        # 3. Clear the Streamlit session state
        for key in ["authenticated", "username", "name", "user_id"]:
            if key in st.session_state:
                del st.session_state[key]

        st.success("You have been securely logged out.")
        # Rerunning forces the app to hit the login page immediately
        st.experimental_rerun()
