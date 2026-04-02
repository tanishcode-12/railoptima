import streamlit as st
from database import create_user, login_user

def login_page():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "username" not in st.session_state:
        st.session_state.username = ""

    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@600;700&family=Nunito:wght@400;600&display=swap');

    html, body, [class*="css"] {
        background-color: #0a0a0f !important;
        color: #e0e0e0 !important;
        font-family: 'Nunito', sans-serif !important;
    }
    .login-header {
        text-align: center;
        padding: 2rem 0 1rem 0;
    }
    .login-header h1 {
        font-family: 'Rajdhani', sans-serif;
        font-size: 3.5rem;
        background: linear-gradient(135deg, #00f5a0, #00d9f5, #a855f7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    .login-header p {
        color: #888;
        font-size: 1rem;
        margin-top: 0.3rem;
    }
    .stTabs [data-baseweb="tab"] {
        color: #aaa !important;
        font-family: 'Nunito', sans-serif !important;
        font-weight: 600 !important;
    }
    .stTabs [aria-selected="true"] {
        color: #00f5a0 !important;
        border-bottom-color: #00f5a0 !important;
    }
    .stTextInput input {
        background: #12121a !important;
        border: 1px solid #2a2a3a !important;
        border-radius: 8px !important;
        color: #e0e0e0 !important;
    }
    .stTextInput input:focus {
        border-color: #00f5a0 !important;
        box-shadow: 0 0 0 2px rgba(0,245,160,0.15) !important;
    }
    .stButton button {
        background: linear-gradient(135deg, #00f5a0, #00d9f5) !important;
        color: #0a0a0f !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 8px !important;
        font-family: 'Nunito', sans-serif !important;
        width: 100% !important;
    }
    .stButton button:hover {
        opacity: 0.9 !important;
        transform: translateY(-1px) !important;
    }
    </style>
    <div class="login-header">
        <h1>🚆 RailOptima</h1>
        <p>Smart Train Fare & Time Optimization</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])

        with tab1:
            username = st.text_input("Username", key="login_user")
            password = st.text_input("Password", type="password", key="login_pass")
            if st.button("Login", key="login_btn"):
                if login_user(username, password):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success("✅ Login Successful!")
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password")

        with tab2:
            new_user = st.text_input("Create Username", key="reg_user")
            new_pass = st.text_input("Create Password", type="password", key="reg_pass")
            if st.button("Register", key="reg_btn"):
                if create_user(new_user, new_pass):
                    st.success("✅ User created! Please login.")
                else:
                    st.error("❌ Username already exists")
