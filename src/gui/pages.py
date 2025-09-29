import streamlit as st
from src.service.auth_service import authenticate_user

# --- Login Component ---

def render_login_form():
    """Displays the login form."""
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.title("Secure Application Login")
        st.markdown("---")
        
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login", type="primary")

            if submitted:
                # authenticate_user now handles token generation, saving to DB, and setting the cookie
                if authenticate_user(username, password):
                    st.success(f"Welcome, {st.session_state.get('name')}! Redirecting...")
                    st.rerun()
                else:
                    st.error("Invalid Username or Password.")
                    
        st.markdown(
            """
            <div style="margin-top: 20px;">
                <p><strong>Test Credentials:</strong></p>
                <p>Username: <code>admin</code></p>
                <p>Password: <code>safe_pass</code></p>
            </div>
            """, 
            unsafe_allow_html=True
        )

# --- Protected Pages ---

def render_dashboard_page():
    """Displays the main protected dashboard content."""
    st.title("📊 Main Dashboard")
    st.markdown("### Secure Data Overview")
    
    st.success(
        f"This content is protected. User: {st.session_state.get('name')} "
        f"({st.session_state.get('username')})"
    )
    
    st.info(
        "**Persistence Check:** Refresh your browser (F5 or Ctrl+R). "
        "The session should be restored automatically via the secure cookie."
    )
    
    st.markdown("""
        <div style="background-color: #f0f2f6; padding: 15px; border-radius: 10px;">
        #### Data Visualizations
        - **Metric 1:** System Uptime 99.9%
        - **Metric 2:** Active Users 42
        - **Chart:** (Placeholder for actual charts)
        </div>
    """, unsafe_allow_html=True)


def render_settings_page():
    """Displays the protected user settings page."""
    st.title("⚙️ Account Settings")
    st.markdown("### Manage User Preferences")
    
    st.warning("Feature under development. This page demonstrates routing for authenticated users.")
    
    st.json({
        "User_ID": st.session_state.get("user_id"),
        "Account_Type": "Admin (Placeholder)",
        "Last_Login_Token": "Verified via secure cookie"
    })
