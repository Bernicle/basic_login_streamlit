import streamlit as st
import os

# Import modules from the production-grade /src structure
# NOTE: These modules must exist in src/service/ and src/gui/ to run.
from src.service.db_manager import init_db
from src.service.auth_service import logout
from src.gui.pages import render_login_form, render_dashboard_page, render_settings_page

# --- Configuration ---
# Define available pages for navigation
PAGES = {
    "Dashboard": render_dashboard_page,
    "Settings": render_settings_page,
}

# --- Initialization and Setup ---

@st.cache_resource(show_spinner="Initializing Database...")
def setup_application():
    """Initializes the database and ensures tables/default users exist."""
    # This function is run once and ensures the 'app_users.db' file and 
    # the default 'admin' user are created securely.
    init_db()
    st.session_state['initialized'] = True
    print("Application setup complete.")

# Ensure DB is initialized before anything else runs
setup_application()

