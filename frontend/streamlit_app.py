import streamlit as st
import streamlit.components.v1 as components
import requests
import uuid
from datetime import datetime

st.set_page_config(
    page_title="ResearchMind AI",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded",   # MUST be expanded so sidebar DOM renders
)

API = "http://localhost:8000"

def auth_headers():
    return {"Authorization": f"Bearer {st.session_state.get('token', '')}"}

def init():
    defaults = {
        "paper_id": None, "filename": None, "uploaded_name": None,
        "summary": None, "sum_length": "medium", "insights": {},
        "chat_history": [], "session_id": str(uuid.uuid4()),
        "dark_mode": False, "token": None, "username": None,
        "logged_in": False, "full_name": None, "auth_page": "login",
        "menu_open": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v
init()

is_dark     = st.session_state.dark_mode
toggle_icon = "🌙" if is_dark else "☀️"

if is_dark:
    theme = """
    --bg-page:#0E0818; --bg-card:#160E24; --bg-surface:#1E1430;
    --bg-elevated:#261B3C; --bg-hover:#2F2249; --bg-input:#1A1028;
    --border:#2A1E42; --border-md:#3A2C58; --border-lt:#4E3E70;
    --text-1:#EDE0FF; --text-2:#C8B0F0; --text-3:#9B7FC0; --text-4:#6B4C9A;
    --primary:#9B7FC0; --primary-hov:#B49ACC; --primary-glow:rgba(155,127,192,0.25);
    --primary-dim:rgba(155,127,192,0.12); --violet:#B49ACC;
    --violet-glow:rgba(180,154,204,0.2); --deep:#6B4C9A; --white:#EDE0FF;
    --nav-bg:rgba(22,14,36,0.85); --app-g1:rgba(92,61,143,0.3);
    --app-g2:rgba(45,27,71,0.4); --footer-border:#2A1E42; --footer-color:#6B4C9A;
    --scbar-track:#160E24; --scbar-thumb:#4E3E70;
    --sb-bg:#100A1C; --sb-border:#2A1E42; --sb-text:#C8B0F0; --sb-hover:#261B3C;
    --ham-bg:rgba(38,27,60,0.95); --ham-border:#3A2C58;
    """
else:
    theme = """
    --bg-page:#EEE6F6; --bg-card:#FFFFFF; --bg-surface:#E4D8F2;
    --bg-elevated:#D8C8EC; --bg-hover:#CCBBE4; --bg-input:#F7F2FC;
    --border:#DDD0EE; --border-md:#C9B8E0; --border-lt:#B49ACC;
    --text-1:#1B0A30; --text-2:#3D2260; --text-3:#6B4C9A; --text-4:#9B7FC0;
    --primary:#5C3D8F; --primary-hov:#4A2D7A; --primary-glow:rgba(92,61,143,0.2);
    --primary-dim:rgba(92,61,143,0.1); --violet:#7B5EA7;
    --violet-glow:rgba(123,94,167,0.2); --deep:#2D1B47; --white:#FFFFFF;
    --nav-bg:rgba(255,255,255,0.75); --app-g1:rgba(196,168,216,0.45);
    --app-g2:rgba(155,127,192,0.25); --footer-border:#DDD0EE; --footer-color:#B49ACC;
    --scbar-track:#E4D8F2; --scbar-thumb:#B49ACC;
    --sb-bg:#F7F2FC; --sb-border:#DDD0EE; --sb-text:#3D2260; --sb-hover:#EDE0FF;
    --ham-bg:rgba(255,255,255,0.95); --ham-border:#C9B8E0;
    """

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Playfair+Display:wght@700&family=JetBrains+Mono:wght@400;500&display=swap');
:root {{ {theme} --r:12px; --r-sm:8px; }}
*, html, body, [class*="css"] {{ font-family:'Inter',sans-serif !important; }}
*, p, span, div, label, h1, h2, h3, h4, h5, h6, [class*="css"], .stMarkdown {{ color:var(--text-1) !important; }}
.stApp {{
    background:var(--bg-page) !important;
    background-image:
        radial-gradient(ellipse 70% 45% at 10% 0%, var(--app-g1) 0%, transparent 65%),
        radial-gradient(ellipse 55% 40% at 90% 100%, var(--app-g2) 0%, transparent 60%) !important;
}}
#MainMenu, footer, header, .stDeployButton {{
    display:none !important; visibility:hidden !important;
}}

/* ══════════════════════════════════
   SIDEBAR
   Hidden by default via CSS (no !important).
   JS inline styles override freely — no fighting.
══════════════════════════════════ */
[data-testid="stSidebarCollapsedControl"] {{
    display: none !important;
}}
[data-testid="stSidebar"] {{
    transform: translateX(-105%);
    visibility: hidden;
    transition: transform 0.26s cubic-bezier(0.4,0,0.2,1), visibility 0.26s;
    background: var(--sb-bg) !important;
    border-right: 1px solid var(--sb-border) !important;
    min-width: 240px !important;
    max-width: 280px !important;
}}
[data-testid="stSidebar"] > div:first-child {{
    padding-top: 1rem !important;
    padding-left: 0.75rem !important;
    padding-right: 0.75rem !important;
}}
[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {{
    gap: 0.1rem !important;
}}
[data-testid="stSidebar"] .stButton {{
    margin-bottom: 0 !important;
    width: 100% !important;
}}
.sidebar-header {{
    font-size: 0.95rem; font-weight: 800;
    color: var(--text-1) !important;
    padding: 0.3rem 0 0.1rem 0.2rem;
    letter-spacing: -0.02em;
}}
.sidebar-divider {{
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--sb-border), transparent);
    margin: 0.6rem 0;
}}
.sidebar-section {{
    font-size: 0.58rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.14em;
    color: var(--text-4) !important;
    margin: 0.7rem 0 0.25rem 0.2rem;
}}
.sb-user-card {{
    background: var(--bg-elevated); border: 1px solid var(--border-md);
    border-radius: 10px; padding: 0.55rem 0.8rem; margin-bottom: 0.25rem;
}}
.sb-user-name {{ font-size:0.82rem; font-weight:700; color:var(--text-1) !important; }}
.sb-user-tag {{
    font-size:0.62rem; color:var(--text-4) !important;
    font-family:'JetBrains Mono',monospace !important; margin-top:1px;
}}
.sb-paper-card {{
    background: var(--primary-dim); border: 1px solid var(--border-md);
    border-radius: 8px; padding: 0.45rem 0.75rem;
    font-size: 0.7rem; color: var(--text-3) !important;
    word-break: break-all; line-height: 1.4;
}}
/* Sidebar buttons — high specificity beats global button styles */
[data-testid="stSidebar"] [data-testid="stVerticalBlock"] .stButton > button,
[data-testid="stSidebar"] [data-testid="stVerticalBlock"] .stButton > button * {{
    background: transparent !important;
    background-image: none !important;
    border: 1px solid transparent !important;
    border-radius: 7px !important;
    color: var(--sb-text) !important;
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    padding: 0.3rem 0.7rem !important;
    width: 100% !important;
    min-height: unset !important;
    height: auto !important;
    line-height: 1.4 !important;
    text-align: left !important;
    box-shadow: none !important;
    transform: none !important;
    transition: background 0.12s, color 0.12s !important;
}}
[data-testid="stSidebar"] [data-testid="stVerticalBlock"] .stButton > button:hover,
[data-testid="stSidebar"] [data-testid="stVerticalBlock"] .stButton > button:hover * {{
    background: var(--sb-hover) !important;
    background-image: none !important;
    border-color: var(--border-md) !important;
    color: var(--primary) !important;
    transform: none !important;
    box-shadow: none !important;
}}
[data-testid="stSidebar"] .st-key-sb_logout button,
[data-testid="stSidebar"] .st-key-sb_logout button * {{
    color: #C47B9B !important;
}}
[data-testid="stSidebar"] .st-key-sb_logout button:hover,
[data-testid="stSidebar"] .st-key-sb_logout button:hover * {{
    color: #e05a85 !important;
    background: rgba(196,123,155,0.08) !important;
    background-image: none !important;
}}

/* ══════════════════════════════════
   HAMBURGER — fixed top-left
══════════════════════════════════ */
.st-key-ham_btn {{
    position: fixed !important; top: 8px !important; left: 8px !important;
    z-index: 999999 !important; height: auto !important; width: auto !important;
    margin: 0 !important; padding: 0 !important;
}}
.st-key-ham_btn button {{
    background: var(--ham-bg) !important;
    border: 1.5px solid var(--ham-border) !important;
    border-radius: 10px !important;
    width: 36px !important; height: 36px !important; min-width: unset !important;
    padding: 0 !important; font-size: 1.05rem !important;
    box-shadow: 0 2px 12px var(--primary-glow) !important;
    cursor: pointer !important; display: flex !important;
    align-items: center !important; justify-content: center !important;
    transform: none !important; color: var(--text-1) !important;
    backdrop-filter: blur(12px) !important; transition: all 0.18s !important;
}}
.st-key-ham_btn button:hover {{
    border-color: var(--primary) !important;
    background: var(--primary-dim) !important;
    transform: scale(1.05) !important;
}}
.st-key-ham_btn button p, .st-key-ham_btn button span {{
    font-size: 1rem !important; line-height: 1 !important; color: var(--text-1) !important;
}}

/* ══════════════════════════════════
   THEME TOGGLE — fixed top-right
══════════════════════════════════ */
.st-key-theme_toggle {{
    position: fixed !important; top: 8px !important; right: 8px !important;
    z-index: 999999 !important; height: auto !important; width: auto !important;
    margin: 0 !important; padding: 0 !important;
}}
.st-key-theme_toggle button {{
    background: var(--ham-bg) !important;
    border: 1.5px solid var(--ham-border) !important;
    border-radius: 50% !important;
    width: 36px !important; height: 36px !important; min-width: unset !important;
    padding: 0 !important; font-size: 1rem !important;
    box-shadow: 0 2px 10px var(--primary-glow) !important;
    cursor: pointer !important; display: flex !important;
    align-items: center !important; justify-content: center !important;
    transform: none !important; backdrop-filter: blur(12px) !important;
    transition: all 0.18s !important;
}}
.st-key-theme_toggle button:hover {{
    border-color: var(--primary) !important;
    background: var(--primary-dim) !important;
    transform: scale(1.1) !important;
}}
.st-key-theme_toggle button p, .st-key-theme_toggle button span {{
    font-size: 1rem !important; line-height: 1 !important;
}}

/* ══════════════════════════════════
   LAYOUT
══════════════════════════════════ */
.block-container {{
    padding-top: 0.6rem !important; padding-left: 2rem !important;
    padding-right: 2rem !important; padding-bottom: 6rem !important;
    max-width: 1100px !important;
}}
::-webkit-scrollbar {{ width:3px; }}
::-webkit-scrollbar-track {{ background:var(--scbar-track); }}
::-webkit-scrollbar-thumb {{ background:var(--scbar-thumb); border-radius:4px; }}

/* ══════════════════════════════════
   NAV BAR
══════════════════════════════════ */
.topnav {{
    display:flex; align-items:center; justify-content:space-between;
    background:var(--nav-bg); border:1px solid var(--border-md);
    border-radius:16px; padding:0.75rem 1.4rem;
    margin:0.4rem auto 1.2rem auto; width:100%;
    backdrop-filter:blur(24px);
    box-shadow:0 4px 24px var(--primary-glow),inset 0 1px 0 rgba(255,255,255,0.08);
}}
.nav-left {{ display:flex; align-items:center; gap:14px; }}
.nav-right {{ display:flex; align-items:center; gap:6px; flex-wrap:wrap; justify-content:flex-end; }}
.nav-icon {{
    width:40px; height:40px;
    background:linear-gradient(135deg,var(--primary) 0%,var(--deep) 100%);
    border-radius:11px; display:flex; align-items:center; justify-content:center;
    font-size:18px; box-shadow:0 4px 16px var(--primary-glow);
}}
.nav-title {{ font-size:1rem; font-weight:800; color:var(--text-1) !important; letter-spacing:-0.02em; }}
.nav-sub {{ font-size:0.67rem; color:var(--text-4) !important; margin-top:2px; }}
.tag {{
    padding:4px 11px; border-radius:20px; font-size:0.67rem; font-weight:600;
    background:var(--bg-surface); color:var(--text-3) !important; border:1px solid var(--border-md);
}}
.tag-on {{ background:var(--primary) !important; color:var(--bg-page) !important; border-color:var(--primary) !important; }}
.sec-label {{ font-size:0.64rem; font-weight:700; text-transform:uppercase; letter-spacing:0.14em; color:var(--violet) !important; margin-bottom:0.3rem; }}
.sec-title {{ font-size:1.05rem; font-weight:800; color:var(--text-1) !important; margin-bottom:0.3rem; letter-spacing:-0.02em; }}
.sec-desc {{ font-size:0.75rem; color:var(--text-3) !important; margin-bottom:1rem; line-height:1.65; }}

/* UPLOAD */
[data-testid="stFileUploader"],[data-testid="stFileUploaderDropzone"] {{
    background:var(--bg-input) !important; border:1.5px dashed var(--border-lt) !important; border-radius:var(--r) !important;
}}
[data-testid="stFileUploader"]:hover,[data-testid="stFileUploaderDropzone"]:hover {{
    border-color:var(--primary) !important; background:var(--primary-dim) !important;
}}
[data-testid="stFileUploaderDropzoneInstructions"] *,[data-testid="stFileUploader"] small,
[data-testid="stFileUploader"] span,[data-testid="stFileUploader"] p {{ color:var(--text-3) !important; }}
[data-testid="stFileUploader"] button {{
    background:var(--bg-elevated) !important; color:var(--text-2) !important;
    border:1px solid var(--border-md) !important; border-radius:var(--r-sm) !important;
    font-weight:600 !important; font-size:0.79rem !important;
}}

/* TABS */
.stTabs [data-baseweb="tab-list"] {{
    background:var(--nav-bg) !important; border:1px solid var(--border-md) !important;
    border-radius:var(--r) !important; padding:5px !important; gap:3px !important;
    box-shadow:0 2px 8px var(--primary-glow) !important;
}}
.stTabs [data-baseweb="tab"] {{
    background:transparent !important; border:none !important;
    border-radius:var(--r-sm) !important; color:var(--text-3) !important;
    font-size:0.82rem !important; font-weight:500 !important; padding:0.46rem 1.2rem !important;
}}
.stTabs [data-baseweb="tab"]:hover {{ color:var(--primary) !important; background:var(--primary-dim) !important; }}
.stTabs [aria-selected="true"],.stTabs [aria-selected="true"] * {{
    background:linear-gradient(135deg,var(--primary) 0%,var(--deep) 100%) !important;
    color:var(--bg-page) !important; font-weight:700 !important;
    box-shadow:0 2px 12px var(--primary-glow) !important;
}}
.stTabs [data-baseweb="tab-panel"] {{ padding:0 !important; padding-top:1.5rem !important; }}

/* BUTTONS */
.stButton > button[kind="primary"],.stButton > button[kind="primary"] * {{ color:var(--bg-page) !important; }}
.stButton > button[kind="primary"] {{
    background:linear-gradient(135deg,var(--primary) 0%,var(--deep) 100%) !important;
    border:none !important; font-weight:700 !important; font-size:0.82rem !important;
    border-radius:var(--r) !important; padding:0.62rem 1rem !important; width:100% !important;
    box-shadow:0 4px 16px var(--primary-glow) !important; transition:all 0.18s !important;
}}
.stButton > button[kind="primary"]:hover {{ transform:translateY(-2px) !important; }}
.stButton > button[kind="secondary"],.stButton > button[kind="secondary"] * {{ color:var(--text-2) !important; }}
.stButton > button[kind="secondary"] {{
    background:var(--bg-card) !important; border:1.5px solid var(--border-md) !important;
    font-weight:500 !important; font-size:0.82rem !important;
    border-radius:var(--r) !important; padding:0.62rem 1rem !important; width:100% !important;
    box-shadow:0 2px 8px var(--primary-glow) !important; transition:all 0.18s !important;
}}
.stButton > button[kind="secondary"]:hover,.stButton > button[kind="secondary"]:hover * {{
    border-color:var(--primary) !important; color:var(--primary) !important; background:var(--primary-dim) !important;
}}
.stButton > button:not([kind]),.stButton > button:not([kind]) * {{ color:var(--bg-page) !important; }}
.stButton > button:not([kind]) {{
    background:linear-gradient(135deg,var(--violet) 0%,var(--primary) 100%) !important;
    font-weight:600 !important; font-size:0.82rem !important;
    border:none !important; border-radius:var(--r) !important;
    padding:0.62rem 1.4rem !important; width:100% !important;
    box-shadow:0 4px 16px var(--violet-glow) !important; transition:all 0.18s !important;
}}
.stButton > button:not([kind]):hover {{ transform:translateY(-2px) !important; }}
.stButton > button:disabled {{ background:var(--bg-elevated) !important; color:var(--text-4) !important; opacity:0.5 !important; }}
.stDownloadButton > button,.stDownloadButton > button * {{ color:var(--text-2) !important; }}
.stDownloadButton > button {{
    background:var(--bg-card) !important; border:1.5px solid var(--border-md) !important;
    border-radius:var(--r-sm) !important; width:auto !important; font-size:0.78rem !important; font-weight:500 !important;
}}
.stDownloadButton > button:hover,.stDownloadButton > button:hover * {{
    border-color:var(--primary) !important; color:var(--primary) !important;
}}

/* TEXT */
.stTextArea textarea {{
    background:var(--bg-input) !important; border:1.5px solid var(--border-md) !important;
    border-radius:var(--r) !important; color:var(--text-1) !important; font-size:0.87rem !important;
}}
.stTextArea textarea::placeholder {{ color:var(--text-4) !important; }}
.stTextArea textarea:focus {{ border-color:var(--violet) !important; box-shadow:0 0 0 3px var(--primary-dim) !important; }}
.stTextArea label {{ font-size:0.64rem !important; font-weight:700 !important; color:var(--text-4) !important; text-transform:uppercase !important; letter-spacing:0.12em !important; }}
.stTextInput input {{ color:#FFFFFF !important; -webkit-text-fill-color:#FFFFFF !important; opacity:1 !important; }}
.stTextInput input::placeholder {{ color:var(--text-4) !important; -webkit-text-fill-color:var(--text-4) !important; opacity:1 !important; }}
.stTextInput input:focus {{ color:#FFFFFF !important; -webkit-text-fill-color:#FFFFFF !important; }}

/* ALERTS */
.stSuccess > div {{ background:var(--primary-dim) !important; border:1px solid var(--border-md) !important; color:var(--primary) !important; }}
.stError > div {{ background:rgba(180,60,100,0.07) !important; border:1px solid rgba(180,60,100,0.25) !important; color:#C47B9B !important; }}
.stWarning > div {{ background:var(--primary-dim) !important; border:1px solid var(--border-md) !important; color:var(--violet) !important; }}
.stInfo > div {{ background:var(--primary-dim) !important; border:1px solid var(--border-md) !important; color:var(--violet) !important; }}
.stSpinner > div {{ border-top-color:var(--primary) !important; }}
[data-testid="stSpinner"] * {{ color:var(--text-2) !important; }}

/* RESULT / INSIGHT / CHAT */
.result-box {{
    background:var(--bg-card); border:1px solid var(--border-md); border-left:4px solid var(--primary);
    border-radius:var(--r); padding:1.4rem 1.6rem; font-size:0.9rem; line-height:1.9;
    color:var(--text-2) !important; margin:0.9rem 0; white-space:pre-wrap;
    box-shadow:0 4px 20px var(--primary-glow);
}}
.result-box * {{ color:var(--text-2) !important; }}
.len-badge {{
    display:inline-block; background:linear-gradient(135deg,var(--primary),var(--deep));
    color:var(--bg-page) !important; border-radius:5px; font-size:0.64rem; font-weight:700;
    padding:2px 9px; margin-left:8px; text-transform:uppercase; letter-spacing:0.1em; vertical-align:middle;
}}
.insight-block {{
    background:var(--bg-card); border:1px solid var(--border-md); border-radius:var(--r);
    padding:1.1rem 1.4rem; margin-bottom:0.8rem; transition:all 0.2s;
    box-shadow:0 2px 8px var(--primary-glow);
}}
.insight-block:hover {{ border-color:var(--violet); box-shadow:0 6px 24px var(--primary-glow); transform:translateY(-2px); }}
.iq {{ font-size:0.65rem; font-weight:700; color:var(--primary) !important; text-transform:uppercase; letter-spacing:0.1em; margin-bottom:0.5rem; font-family:'JetBrains Mono',monospace !important; }}
.ia {{ font-size:0.88rem; color:var(--text-2) !important; line-height:1.8; }}
.chat-you {{ display:flex; justify-content:flex-end; margin-bottom:0.65rem; }}
.chat-ai {{ display:flex; justify-content:flex-start; margin-bottom:0.65rem; }}
.bub-you {{
    background:linear-gradient(135deg,var(--primary) 0%,var(--deep) 100%);
    color:var(--bg-page) !important; border-radius:16px 16px 4px 16px;
    padding:0.75rem 1.15rem; font-size:0.86rem; max-width:74%; line-height:1.7; font-weight:500;
    box-shadow:0 4px 16px var(--primary-glow);
}}
.bub-you * {{ color:var(--bg-page) !important; }}
.bub-ai {{
    background:var(--bg-card); color:var(--text-2) !important;
    border:1px solid var(--border-md); border-radius:16px 16px 16px 4px;
    padding:0.75rem 1.15rem; font-size:0.86rem; max-width:74%; line-height:1.7;
    box-shadow:0 2px 10px var(--primary-glow);
}}
.bub-ai * {{ color:var(--text-2) !important; }}
.chat-lbl {{ font-size:0.61rem; font-weight:700; letter-spacing:0.1em; text-transform:uppercase; color:var(--text-4) !important; margin-bottom:0.22rem; padding:0 4px; font-family:'JetBrains Mono',monospace !important; }}
.chat-lbl-r {{ text-align:right; }}
.empty {{ text-align:center; padding:4rem 1rem; }}
.empty-icon {{ font-size:2.5rem; margin-bottom:0.8rem; }}
.empty-title {{ font-size:0.92rem; font-weight:700; color:var(--text-3) !important; margin-bottom:0.4rem; }}
.empty-sub {{ font-size:0.77rem; color:var(--text-4) !important; line-height:1.75; }}
.divider {{ height:1px; background:linear-gradient(90deg,transparent,var(--border-md),transparent); margin:1.2rem 0; }}

/* AUTH */
.auth-wrap {{
    max-width:420px; margin:3rem auto 0 auto;
    background:var(--bg-card); border:1px solid var(--border-md);
    border-radius:20px; padding:2.8rem 2.4rem 2.4rem;
    box-shadow:0 8px 40px var(--primary-glow);
}}
.auth-icon {{
    width:56px; height:56px;
    background:linear-gradient(135deg,var(--primary) 0%,var(--deep) 100%);
    border-radius:15px; display:flex; align-items:center; justify-content:center;
    font-size:26px; margin:0 auto 1.2rem auto; box-shadow:0 4px 20px var(--primary-glow);
}}
.auth-title {{ font-size:1.3rem; font-weight:800; color:var(--text-1) !important; text-align:center; letter-spacing:-0.02em; margin-bottom:0.3rem; }}
.auth-sub {{ font-size:0.76rem; color:var(--text-4) !important; text-align:center; margin-bottom:1.8rem; }}
.auth-switch {{ text-align:center; font-size:0.75rem; color:var(--text-4) !important; margin-top:1rem; }}
.auth-footer {{ text-align:center; font-size:0.65rem; color:var(--text-4) !important; margin-top:1.2rem; letter-spacing:0.06em; }}
.auth-divider {{ height:1px; background:linear-gradient(90deg,transparent,var(--border-md),transparent); margin:1rem 0; }}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
# SIDEBAR — ALWAYS rendered unconditionally.
# JS purely slides it in/out — no st.sidebar toggle clicks.
# ══════════════════════════════════════════════════════
with st.sidebar:
    st.markdown('<div class="sidebar-header">🔮 ResearchMind AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

    if st.session_state.logged_in:
        _uname = st.session_state.username or ""
        _fname = st.session_state.full_name or _uname
        st.markdown(f"""
        <div class="sb-user-card">
            <div class="sb-user-name">👤 &nbsp;{_fname}</div>
            <div class="sb-user-tag">@{_uname}</div>
        </div>""", unsafe_allow_html=True)

    if st.session_state.paper_id:
        st.markdown('<div class="sidebar-section">Active Paper</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="sb-paper-card">📄 &nbsp;{st.session_state.filename}</div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">Navigation</div>', unsafe_allow_html=True)

    if st.button("💬  Chat History",  key="sb_history",    use_container_width=True):
        st.session_state.menu_open = False; st.rerun()
    if st.button("📄  New Upload",    key="sb_new_upload", use_container_width=True):
        for k in ["paper_id","filename","uploaded_name","summary","insights","chat_history"]:
            st.session_state[k] = None if k not in ["insights","chat_history"] else ({} if k=="insights" else [])
        st.session_state.menu_open = False; st.rerun()
    if st.button("🗑️  Clear Chat",    key="sb_clear_chat", use_container_width=True):
        st.session_state.chat_history = []; st.session_state.session_id = str(uuid.uuid4())
        st.session_state.menu_open = False; st.rerun()

    st.markdown('<div class="sidebar-section">Info</div>', unsafe_allow_html=True)
    if st.button("❓  Help",          key="sb_help",       use_container_width=True):
        st.session_state.menu_open = False; st.rerun()
    if st.button("ℹ️  About",         key="sb_about",      use_container_width=True):
        st.session_state.menu_open = False; st.rerun()

    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-section">Account</div>', unsafe_allow_html=True)

    if st.button("⎋  Logout",         key="sb_logout",     use_container_width=True):
        for k in ["logged_in","token","username","full_name","paper_id","filename",
                  "uploaded_name","summary","insights","chat_history","menu_open"]:
            st.session_state[k] = False if k in ["logged_in","menu_open"] else None
        st.rerun()
    if st.button("✕  Close",          key="sb_close",      use_container_width=True):
        st.session_state.menu_open = False; st.rerun()


# ══════════════════════════════════════════════════════
# JS — slide sidebar in/out via CSS transform.
# Inline styles always beat stylesheet rules (no !important conflict).
# Zero toggle clicks → zero extra reruns → no double-click.
# ══════════════════════════════════════════════════════
_open = "true" if st.session_state.menu_open else "false"
components.html(f"""
<script>
(function() {{
    var show = {_open};
    function apply() {{
        var sb = window.parent.document.querySelector('[data-testid="stSidebar"]');
        if (!sb) {{ setTimeout(apply, 30); return; }}
        if (show) {{
            sb.style.transform  = 'none';
            sb.style.visibility = 'visible';
        }} else {{
            sb.style.transform  = 'translateX(-105%)';
            sb.style.visibility = 'hidden';
        }}
    }}
    apply();
}})();
</script>
""", height=0)


# ══════════════════════════════════════════════════════
# HAMBURGER — fixed top-left
# ══════════════════════════════════════════════════════
ham_icon = "✕" if st.session_state.menu_open else "☰"
if st.button(ham_icon, key="ham_btn"):
    st.session_state.menu_open = not st.session_state.menu_open
    st.rerun()

# ══════════════════════════════════════════════════════
# THEME TOGGLE — fixed top-right
# ══════════════════════════════════════════════════════
if st.button(toggle_icon, key="theme_toggle"):
    st.session_state.dark_mode = not st.session_state.dark_mode
    st.rerun()


# ══════════════════════════════════════════════════════
# AUTH PAGES
# ══════════════════════════════════════════════════════
if not st.session_state.logged_in:
    if st.session_state.auth_page == "login":
        st.markdown("""
        <div class="auth-wrap">
            <div class="auth-icon">🔮</div>
            <div class="auth-title">Welcome Back</div>
            <div class="auth-sub">Sign in to access ResearchMind AI</div>
        </div>""", unsafe_allow_html=True)
        _, col, _ = st.columns([1, 2, 1])
        with col:
            username = st.text_input("Username", placeholder="Enter your username", key="login_user")
            password = st.text_input("Password", placeholder="Enter your password", type="password", key="login_pass")
            if st.button("Sign In →", key="login_btn"):
                if username.strip() and password.strip():
                    with st.spinner("Signing in…"):
                        res = requests.post(f"{API}/login", json={"username": username.strip(), "password": password.strip()})
                    if res.status_code == 200:
                        data = res.json()
                        st.session_state.token     = data["access_token"]
                        st.session_state.username  = data["username"]
                        st.session_state.full_name = data["full_name"]
                        st.session_state.logged_in = True
                        st.rerun()
                    else:
                        st.error("Invalid username or password.")
                else:
                    st.warning("Please enter both username and password.")
            st.markdown('<div class="auth-divider"></div>', unsafe_allow_html=True)
            st.markdown("<div class='auth-switch'>Don't have an account?</div>", unsafe_allow_html=True)
            if st.button("Create Account →", key="go_register"):
                st.session_state.auth_page = "register"; st.rerun()
            st.markdown("<div class='auth-footer'>RESEARCHMIND AI &nbsp;·&nbsp; FASTAPI &nbsp;·&nbsp; FAISS &nbsp;·&nbsp; GROQ</div>", unsafe_allow_html=True)

    elif st.session_state.auth_page == "register":
        st.markdown("""
        <div class="auth-wrap">
            <div class="auth-icon">✦</div>
            <div class="auth-title">Create Account</div>
            <div class="auth-sub">Join ResearchMind AI — it's free</div>
        </div>""", unsafe_allow_html=True)
        _, col, _ = st.columns([1, 2, 1])
        with col:
            reg_fullname = st.text_input("Full Name",        placeholder="e.g. Karthick Bala",  key="reg_name")
            reg_username = st.text_input("Username",         placeholder="e.g. karthickbala",   key="reg_user")
            reg_password = st.text_input("Password",         placeholder="Min 6 characters",    type="password", key="reg_pass")
            reg_confirm  = st.text_input("Confirm Password", placeholder="Re-enter password",   type="password", key="reg_confirm")
            if st.button("Create Account →", key="register_btn"):
                if not all([reg_fullname.strip(), reg_username.strip(), reg_password.strip(), reg_confirm.strip()]):
                    st.warning("Please fill in all fields.")
                elif reg_password != reg_confirm:
                    st.error("Passwords do not match.")
                elif len(reg_password) < 6:
                    st.error("Password must be at least 6 characters.")
                else:
                    with st.spinner("Creating your account…"):
                        res = requests.post(f"{API}/register", json={
                            "username": reg_username.strip(), "full_name": reg_fullname.strip(),
                            "password": reg_password.strip(), "confirm_password": reg_confirm.strip()
                        })
                    if res.status_code == 200:
                        st.success(f"✅ Account created! Welcome, {reg_fullname.strip()}! Please sign in.")
                        st.session_state.auth_page = "login"; st.rerun()
                    elif res.status_code == 409:
                        st.error("Username already exists.")
                    else:
                        st.error(f"Registration failed: {res.json().get('detail', 'Unknown error')}")
            st.markdown('<div class="auth-divider"></div>', unsafe_allow_html=True)
            st.markdown('<div class="auth-switch">Already have an account?</div>', unsafe_allow_html=True)
            if st.button("← Back to Sign In", key="go_login"):
                st.session_state.auth_page = "login"; st.rerun()
            st.markdown("<div class='auth-footer'>RESEARCHMIND AI &nbsp;·&nbsp; FASTAPI &nbsp;·&nbsp; FAISS &nbsp;·&nbsp; GROQ</div>", unsafe_allow_html=True)
    st.stop()


# ══════════════════════════════════════════════════════
# MAIN APP
# ══════════════════════════════════════════════════════
status = (f'<span class="tag tag-on">✦ &nbsp;{st.session_state.filename}</span>'
          if st.session_state.paper_id else '<span class="tag">No paper loaded</span>')
st.markdown(f"""
<div class="topnav">
  <div class="nav-left">
    <div class="nav-icon">🔮</div>
    <div>
      <div class="nav-title">ResearchMind AI</div>
      <div class="nav-sub">Upload · Summarize · Insights · Chat</div>
    </div>
  </div>
  <div class="nav-right">
    <span class="tag">Groq LLM</span><span class="tag">FAISS</span>
    {status}
    <span class="tag tag-on">👤 &nbsp;{st.session_state.username}</span>
  </div>
</div>
""", unsafe_allow_html=True)

_hour  = datetime.now().hour
_greet = "Good morning" if _hour < 12 else "Good afternoon" if _hour < 18 else "Good evening"
_name  = st.session_state.full_name or st.session_state.username or ""
st.markdown(f"""
<style>
.greeting-text {{ font-size:2.2rem; font-weight:700; font-family:'Playfair Display',serif !important; color:var(--text-1) !important; text-align:center; letter-spacing:-0.01em; margin-bottom:0.4rem; }}
.greeting-sub {{ font-size:0.82rem; color:var(--text-4) !important; text-align:center; letter-spacing:0.04em; margin-bottom:1.5rem; }}
</style>
<div class="greeting-text">{_greet}, {_name} 👋</div>
<div class="greeting-sub">What would you like to research today?</div>
""", unsafe_allow_html=True)

st.markdown('<div class="sec-label">Step 1 — Get Started</div>', unsafe_allow_html=True)
st.markdown('<div class="sec-title">Upload Your Research Paper</div>', unsafe_allow_html=True)
st.markdown('<div class="sec-desc">PDF only · Max 200MB · Indexed instantly for semantic search & AI analysis</div>', unsafe_allow_html=True)

uploaded = st.file_uploader("Upload", type=["pdf"], label_visibility="collapsed")
if uploaded is not None and uploaded.name != st.session_state.uploaded_name:
    with st.spinner("Uploading and indexing your paper…"):
        res = requests.post(f"{API}/upload", files={"file": uploaded}, headers=auth_headers())
    if res.status_code == 200:
        data = res.json()
        st.session_state.paper_id      = data["paper_id"]
        st.session_state.filename      = uploaded.name
        st.session_state.uploaded_name = uploaded.name
        st.session_state.summary       = None
        st.session_state.sum_length    = "medium"
        st.session_state.insights      = {}
        st.session_state.chat_history  = []
        st.session_state.session_id    = str(uuid.uuid4())
        st.success(f"✅ {uploaded.name} — uploaded and indexed successfully.")
    else:
        st.error(f"Upload failed ({res.status_code}). Please try again.")

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

if not st.session_state.paper_id:
    st.markdown("""
    <div class="empty">
      <div class="empty-icon">🔮</div>
      <div class="empty-title">Ready when you are</div>
      <div class="empty-sub">Upload a research paper above to unlock<br>AI-powered Summary, Insights, and Chat.</div>
    </div>""", unsafe_allow_html=True)
else:
    tab1, tab2, tab3 = st.tabs(["✦  Summary", "◈  Insights", "◉  Chat"])

    with tab1:
        st.markdown('<div class="sec-title">AI Summary</div>', unsafe_allow_html=True)
        st.markdown('<div class="sec-desc">Select a length and let the AI distill your paper.</div>', unsafe_allow_html=True)
        st.markdown('<div class="sec-label">Summary Length</div>', unsafe_allow_html=True)
        l1, l2, l3 = st.columns(3)
        lengths = {"short":("⚡","Short","3 sentences"),"medium":("◈","Medium","2 paragraphs"),"long":("◉","Long","5 paragraphs")}
        for col, key in zip([l1,l2,l3], ["short","medium","long"]):
            icon, name, desc = lengths[key]
            with col:
                is_active = st.session_state.sum_length == key
                if st.button(f"{icon} {name}\n{desc}", key=f"lb_{key}", use_container_width=True,
                             type="primary" if is_active else "secondary"):
                    if not is_active:
                        st.session_state.sum_length = key; st.session_state.summary = None; st.rerun()
        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
        if st.session_state.summary is None:
            desc_map = {"short":"3 sentences","medium":"2 paragraphs","long":"5 paragraphs"}
            if st.button(f"✦ Generate Summary  ·  {desc_map[st.session_state.sum_length]}", key="gen_btn"):
                with st.spinner(f"Generating {st.session_state.sum_length} summary…"):
                    res = requests.post(f"{API}/summarize", json={"paper_id": st.session_state.paper_id, "length": st.session_state.sum_length}, headers=auth_headers())
                if res.status_code == 200:
                    st.session_state.summary = res.json().get("summary",""); st.rerun()
                else:
                    st.error("Summarization failed.")
        else:
            badge = st.session_state.sum_length.upper()
            st.markdown(f'<p style="font-size:0.7rem;color:var(--text-3);margin:0.5rem 0 0.2rem">RESULT <span class="len-badge">{badge}</span></p>', unsafe_allow_html=True)
            st.markdown(f'<div class="result-box">{st.session_state.summary}</div>', unsafe_allow_html=True)
            c1, c2, _ = st.columns([1.4, 1.7, 2.9])
            with c1:
                if st.button("↺ Regenerate", key="regen_btn"):
                    with st.spinner("Regenerating…"):
                        res = requests.post(f"{API}/summarize", json={"paper_id": st.session_state.paper_id, "length": st.session_state.sum_length}, headers=auth_headers())
                    if res.status_code == 200:
                        st.session_state.summary = res.json().get("summary",""); st.rerun()
            with c2:
                st.download_button("⬇ Download .txt", st.session_state.summary, file_name=f"summary_{st.session_state.sum_length}.txt")

    with tab2:
        st.markdown('<div class="sec-title">Extract Insights</div>', unsafe_allow_html=True)
        st.markdown('<div class="sec-desc">One question per line — answers retrieved directly from your paper.</div>', unsafe_allow_html=True)
        q_input = st.text_area("Questions",
            placeholder="What is the main research problem?\nWhat methods were used?\nWhat are the key findings?\nWhat are the limitations?",
            height=140, label_visibility="collapsed")
        if st.button("◈ Extract Insights", key="ins_btn"):
            qs = [q.strip() for q in q_input.split("\n") if q.strip()]
            if qs:
                with st.spinner(f"Extracting insights from {len(qs)} question(s)…"):
                    res = requests.post(f"{API}/insights", json={"paper_id": st.session_state.paper_id, "questions": qs}, headers=auth_headers())
                if res.status_code == 200:
                    st.session_state.insights = res.json().get("insights",{}); st.rerun()
                else:
                    st.error("Failed. Please try again.")
            else:
                st.warning("Enter at least one question.")
        if st.session_state.insights:
            st.markdown("<br>", unsafe_allow_html=True)
            for q, a in st.session_state.insights.items():
                st.markdown(f'<div class="insight-block"><div class="iq">◈ {q}</div><div class="ia">{a}</div></div>', unsafe_allow_html=True)
            export = "\n\n".join([f"Q: {q}\nA: {a}" for q, a in st.session_state.insights.items()])
            st.download_button("⬇ Download Insights .txt", export, file_name="insights.txt")

    with tab3:
        st.markdown('<div class="sec-title">Chat with Paper</div>', unsafe_allow_html=True)
        st.markdown('<div class="sec-desc">Ask anything — the AI reads your full PDF and remembers every exchange.</div>', unsafe_allow_html=True)
        chat_box = st.container(height=440, border=False)
        with chat_box:
            if not st.session_state.chat_history:
                st.markdown("""<div class="empty"><div class="empty-icon">◉</div>
                <div class="empty-title">Conversation is empty</div>
                <div class="empty-sub">Ask the AI anything about your paper.</div></div>""", unsafe_allow_html=True)
            else:
                for msg in st.session_state.chat_history:
                    if msg["role"] == "user":
                        st.markdown(f'<div class="chat-lbl chat-lbl-r">You</div><div class="chat-you"><div class="bub-you">{msg["content"]}</div></div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="chat-lbl">ResearchMind</div><div class="chat-ai"><div class="bub-ai">{msg["content"]}</div></div>', unsafe_allow_html=True)
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        user_msg = st.text_area("Message", placeholder="e.g. What is the core contribution of this paper?",
                                height=82, label_visibility="collapsed", key="chat_input")
        c1, c2 = st.columns([4, 1])
        with c1:
            send = st.button("Send Message →", key="send_btn")
        with c2:
            if st.button("⊗ Clear", key="clear_btn"):
                st.session_state.chat_history = []; st.session_state.session_id = str(uuid.uuid4()); st.rerun()
        if send:
            if user_msg.strip():
                st.session_state.chat_history.append({"role":"user","content":user_msg.strip()})
                with st.spinner("Reading paper and composing answer…"):
                    res = requests.post(f"{API}/chat", json={"session_id": st.session_state.session_id, "message": user_msg.strip(), "paper_id": st.session_state.paper_id}, headers=auth_headers())
                if res.status_code == 200:
                    reply = res.json().get("response","Sorry, no response.")
                    st.session_state.chat_history.append({"role":"assistant","content":reply}); st.rerun()
                else:
                    st.error("Chat failed. Please try again.")
            else:
                st.warning("Please type a message first.")

st.markdown("""
<div style="text-align:center;margin-top:5rem;padding-top:1.2rem;
     border-top:1px solid var(--footer-border);font-size:0.65rem;
     color:var(--footer-color);letter-spacing:0.1em;font-family:'JetBrains Mono',monospace;">
    RESEARCHMIND AI &nbsp;·&nbsp; FASTAPI &nbsp;·&nbsp; FAISS &nbsp;·&nbsp; GROQ LLM &nbsp;·&nbsp; STREAMLIT
</div>
""", unsafe_allow_html=True)