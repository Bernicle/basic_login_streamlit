import streamlit as st
import os

# Import modules from the production-grade /src structure
from src.service.db_manager import init_db
# 🚨 IMPORT: Get the new cookie-aware functions
from src.service.auth_service import logout, check_cookie_authentication 
from src.gui.pages import render_login_form, render_dashboard_page, render_settings_page

# --- Configuration ---
PAGES = {
    "Dashboard": render_dashboard_page,
    "Settings": render_settings_page,
}

# --- Initialization and Setup ---

@st.cache_resource(show_spinner="Initializing Database...")
def setup_application():
    """Initializes the database and ensures tables/default users exist."""
    init_db()
    st.session_state['initialized'] = True
    print("Application setup complete.")

# Ensure DB is initialized before anything else runs
setup_application()

# --- Application Main Flow ---

def main():
    st.set_page_config(
        page_title="Production-Grade Streamlit App",
        layout="wide"
    )

    # 🚨 CRITICAL FIX FOR PERSISTENCE: 
    # Check the cookie immediately on every run. If a valid token is found,
    # it restores the st.session_state['authenticated'] = True, keeping the user logged in.
    check_cookie_authentication() 

    # --- SESSION STATE INITIALIZATION (Defaulting) ---
    # Ensure all required state variables are initialized. If check_cookie_authentication 
    # restored the state, these checks will pass without resetting the values.
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False
    if 'current_page' not in st.session_state:
        st.session_state['current_page'] = "Dashboard" 
    if 'name' not in st.session_state:
        st.session_state['name'] = 'N/A'
    
    
    if st.session_state['authenticated']:
        # === PROTECTED VIEW ===

        # 1. Sidebar Navigation and Logout
        with st.sidebar:
            st.title("Application Menu")
            st.subheader(f"User: {st.session_state.get('name')}") 
            
            page_selection = st.radio(
                "Navigate",
                list(PAGES.keys()),
                index=list(PAGES.keys()).index(st.session_state['current_page']),
                key="page_selector"
            )
            st.session_state['current_page'] = page_selection

            st.markdown("---")
            if st.button("Logout", type="secondary"):
                logout()

        # 2. Render Current Page Content
        PAGES[st.session_state['current_page']]()

    else:
        # === PUBLIC VIEW (Login) ===
        render_login_form()

if __name__ == '__main__':
    main()
