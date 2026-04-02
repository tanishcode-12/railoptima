import streamlit as st
from login import login_page
from page1 import show_page1
from page2 import show_page2

st.set_page_config(
    page_title="RailOptima",
    page_icon="🚆",
    layout="wide"
)

# ── Global dark styles + sidebar ──────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@600;700&family=Nunito:wght@400;600;700&display=swap');

html, body, [class*="css"] {
    background-color: #0a0a0f !important;
    color: #e0e0e0 !important;
    font-family: 'Nunito', sans-serif !important;
}
section[data-testid="stSidebar"] {
    background: #0d0d14 !important;
    border-right: 1px solid #1e1e2e !important;
}
section[data-testid="stSidebar"] * {
    color: #e0e0e0 !important;
}
.sidebar-brand {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.8rem;
    font-weight: 700;
    background: linear-gradient(135deg, #00f5a0, #00d9f5, #a855f7);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.sidebar-user {
    color: #aaa !important;
    font-size: 0.9rem;
    margin-bottom: 0.5rem;
}
.sidebar-user span {
    color: #00f5a0;
    font-weight: 700;
}
[data-testid="stSidebarNav"] { display: none !important; }
div[data-testid="stRadio"] label {
    font-family: 'Nunito', sans-serif !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    padding: 0.4rem 0 !important;
    color: #ccc !important;
}
div[data-testid="stRadio"] label:hover { color: #00f5a0 !important; }

.stButton > button {
    transition: all 0.2s ease !important;
}
</style>
""", unsafe_allow_html=True)

# ── Login Gate ────────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login_page()

else:
    # ── Init session state ────────────────────────────────
    if "page" not in st.session_state:
        st.session_state.page = "🚆 Train Planner"
    if "top_train" not in st.session_state:
        st.session_state.top_train = None

    # ── Sidebar ───────────────────────────────────────────
    with st.sidebar:
        st.markdown('<div class="sidebar-brand">🚆 RailOptima</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="sidebar-user">👤 Welcome, <span>{st.session_state.username}</span></div>', unsafe_allow_html=True)
        st.divider()

        pages = ["🚆 Train Planner", "📊 Analytics & Insights"]

        # Sync radio with session state page
        current_index = pages.index(st.session_state.page) if st.session_state.page in pages else 0

        selected = st.radio(
            "Navigate",
            pages,
            index=current_index,
            label_visibility="collapsed"
        )

        # Update page in session state when radio changes
        if selected != st.session_state.page:
            st.session_state.page = selected
            st.rerun()

        st.divider()

        if st.button("🚪 Logout", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    # ── Page Routing ──────────────────────────────────────
    if st.session_state.page == "🚆 Train Planner":
        show_page1()
    elif st.session_state.page == "📊 Analytics & Insights":
        show_page2()
