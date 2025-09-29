import streamlit as st
from src.service.auth_service import authenticate_user, logout

# --- Dashboard & Protected Pages ---

def render_dashboard_page():
    """Renders the main protected dashboard content."""
    st.title("Main Data Dashboard 📈")
    st.header(f"Welcome back, {st.session_state.get('name', 'User')}!")
    st.success("You are securely logged in.")
    
    st.markdown("---")
    st.subheader("Data Overview")
    st.write("This is a production-grade secured dashboard.")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("KPI 1 (Today)", "4,500", "+12%")
    col2.metric("KPI 2 (Active Users)", "12", "-5")
    col3.metric("DB Status", "Connected", "OK")

def render_settings_page():
    """Renders the protected settings page."""
    st.title("⚙️ Application Settings")
    st.subheader(f"User ID: {st.session_state.get('user_id')}")
    st.info("Here you can configure application parameters.")
    
    st.text_input("Application Name", "Flood Monitor v1.0")
    st.slider("Refresh Rate (seconds)", 1, 60, 10)
    st.button("Save Configuration", type="primary")

# --- Login Component ---

def render_login_form():
    """Renders the login form in the main content area."""
    st.title("Secure Application Login")
    st.subheader("Please sign in to continue")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login", type="primary")

        if submitted:
            # Call the central authentication service
            if authenticate_user(username, password):
                st.success("Login successful! Redirecting...")
                st.rerun()
            else:
                st.error("Invalid Username or Password.")
    
    st.markdown("---")
    st.caption("Demo Account: admin / safe_pass")
