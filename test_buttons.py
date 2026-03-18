import streamlit as st

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

# ---- init state ----
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False
if "menu_open" not in st.session_state:
    st.session_state.menu_open = False

is_dark     = st.session_state.dark_mode
theme_label = "☀️ Light" if is_dark else "🌙 Dark"

# ---- CSS ----
st.markdown("""
<style>
.block-container { padding-top: 0rem !important; }
[data-testid="stSidebarCollapsedControl"] { display: none !important; }

.ham-btn > div > button {
    position: fixed !important;
    top: 10px !important;
    left: 10px !important;
    z-index: 9999 !important;
    background: #f0f0f0 !important;
    border: 1.5px solid #ccc !important;
    border-radius: 8px !important;
    padding: 5px 11px !important;
    font-size: 1.1rem !important;
    width: auto !important;
    min-width: unset !important;
}

.theme-btn > div > button {
    position: fixed !important;
    top: 10px !important;
    right: 10px !important;
    z-index: 9999 !important;
    background: #f0f0f0 !important;
    border: 1.5px solid #ccc !important;
    border-radius: 20px !important;
    padding: 5px 14px !important;
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    width: auto !important;
    min-width: unset !important;
}

[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    border: 1px solid transparent !important;
    border-radius: 8px !important;
    padding: 0.55rem 0.8rem !important;
    font-size: 0.84rem !important;
    width: 100% !important;
    box-shadow: none !important;
    transform: none !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: #f0eeff !important;
    transform: none !important;
}
</style>
""", unsafe_allow_html=True)

# ---- SIDEBAR FIRST ---- ← KEY: must be before hamburger button
if st.session_state.menu_open:
    with st.sidebar:
        st.markdown("### 🔮 Menu")
        st.markdown("---")
        st.button("💬  Chat History", key="menu_history", use_container_width=True)
        st.button("❓  Help",         key="menu_help",    use_container_width=True)
        st.button("ℹ️  About",        key="menu_about",   use_container_width=True)
        st.markdown("---")
        if st.button("⎋  Logout", key="menu_logout", use_container_width=True):
            st.write("Logged out!")
        if st.button("✕  Close Menu", key="menu_close", use_container_width=True):
            st.session_state.menu_open = False
            st.rerun()

# ---- HAMBURGER BUTTON ----
st.markdown('<div class="ham-btn">', unsafe_allow_html=True)
if st.button("☰", key="ham_btn"):
    st.session_state.menu_open = not st.session_state.menu_open
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# ---- THEME BUTTON ----
st.markdown('<div class="theme-btn">', unsafe_allow_html=True)
if st.button(theme_label, key="theme_btn"):
    st.session_state.dark_mode = not st.session_state.dark_mode
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# ---- MAIN CONTENT ----
st.title("🔮 ResearchMind AI")
st.write(f"Dark mode is: {'ON 🌙' if is_dark else 'OFF ☀️'}")