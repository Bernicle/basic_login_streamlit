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

# --- Application Main Flow ---

def main():
    st.set_page_config(
        page_title="Production-Grade Streamlit App",
        layout="wide"
    )

    # Initialize session state variables if they don't exist
    if 'authenticated' not in st.session_state:
        # Default state: user is not logged in
        st.session_state['authenticated'] = False
        st.session_state['current_page'] = "Dashboard" # Default page after login

    if st.session_state['authenticated']:
        # === PROTECTED VIEW: Display navigation and content ===

        # 1. Sidebar Navigation and Logout
        with st.sidebar:
            st.title("Application Menu")
            # Display authenticated user's name
            st.subheader(f"User: {st.session_state.get('name', 'N/A')}") 
            
            # Navigation Radio Button
            page_selection = st.radio(
                "Navigate",
                list(PAGES.keys()),
                # Use key and current_page state for sticky navigation selection
                index=list(PAGES.keys()).index(st.session_state['current_page']),
                key="page_selector"
            )
            st.session_state['current_page'] = page_selection

            st.markdown("---")
            if st.button("Logout", type="secondary"):
                logout() # Calls the service function to clear state and rerun

        # 2. Render Current Page Content using the routing dictionary
        PAGES[st.session_state['current_page']]()

    else:
        # === PUBLIC VIEW: Display the Login Form ===
        render_login_form()

if __name__ == '__main__':
    main()
