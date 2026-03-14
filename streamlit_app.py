"""
UV Sun Safety Awareness Platform
A Streamlit app for young Australians aged 18-24
"""

import streamlit as st

# Page configuration
st.set_page_config(
    page_title="UVsense Australia",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

PAGES = {
    "dashboard": "Dashboard",
    "uv-awareness": "UV Awareness",
    "skin-type-tool": "Skin Type Tool",
    "protection-planner": "Protection Planner",
    "reminder-settings": "Reminder Settings",
}

# Custom CSS
st.markdown("""
<style>
    .stApp {
    background: linear-gradient(180deg, #fffaf5 0%, #fffdf8 55%, #ffffff 100%);
    }

    .stButton > button {
    background: white;
    color: #334155;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 0.65rem 1rem;
    font-weight: 600;
    min-height: 44px;
    box-shadow: none;
    }

    .stButton > button:hover {
    border-color: #f97316;
    color: #ea580c;
    background: #fff7ed;
    }

    .card,
    .protection-card {
    background: rgba(255,255,255,0.92);
    padding: 1.35rem;
    border-radius: 8px;
    border: 1px solid rgba(15, 23, 42, 0.06);
    box-shadow: 0 6px 24px rgba(15, 23, 42, 0.05);
    }

    .uv-gauge {
        background: white;
        border: 4px solid transparent;
        border-radius: 50%;
        width: 260px;
        height: 260px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin: 2rem auto;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }

    .uv-number {
        font-size: 7rem !important;
        font-weight: 700 !important;
        margin: 0 !important;
        line-height: 1 !important;
    }

    .uv-label {
        font-size: 0.875rem;
        color: #6b7280;
        margin: 0;
    }

    .uv-level {
        font-size: 1.25rem;
        font-weight: 600;
        margin: 0.5rem 0 0 0;
    }

    .warning-banner {
        color: white;
        padding: 0.95rem 1rem;
        border-radius: 8px;
        text-align: center;
        margin: 1.5rem auto;
        max-width: 700px;
        font-weight: 500;
    }

    .icon-circle {
        width: 48px;
        height: 48px;
        border-radius: 50%;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 1rem;
    }
    
    .navbar {
    display: flex;
    gap: 2rem;
    margin: 0.4rem 0 1.8rem 0;
    align-items: center;
    border-bottom: 1px solid rgba(0, 0, 0, 0.06);
    padding-bottom: 0.75rem;
    flex-wrap: wrap;
    }

    .nav-item {
    display: inline-block;
    text-decoration: none !important;
    color: #475569 !important;
    font-size: 0.98rem;
    font-weight: 600;
    padding: 0.25rem 0.1rem 0.7rem 0.1rem;
    border: none;
    border-bottom: 2px solid transparent;
    border-radius: 0;
    background: transparent;
    transition: all 0.18s ease;
    padding-bottom:0.65rem;
    }

    .nav-item:hover {
    color: #ea580c !important;
    text-decoration: none !important;
    }

    .nav-item.active {
    color: #ea580c !important;
    border-bottom: 3px solid #fb923c;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    [data-testid="stSidebar"] {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

# Session state
query_page = st.query_params.get("page", "dashboard")

if query_page not in PAGES:
    query_page = "dashboard"

if "page" not in st.session_state:
    st.session_state.page = query_page
else:
    st.session_state.page = query_page

def render_top_nav(current_page):
    nav_items = [
        ("dashboard", "Dashboard"),
        ("uv-awareness", "UV Awareness"),
        ("skin-type-tool", "Skin Type Tool"),
        ("protection-planner", "Protection Planner"),
        ("reminder-settings", "Reminder Settings"),
    ]

    nav_html = "<div class='navbar'>"

    for slug, label in nav_items:
        active_class = "active" if current_page == slug else ""
        nav_html += f"""<a class="nav-item {active_class}" href="?page={slug}" target="_self">{label}</a>"""

    nav_html += "</div>"

    st.markdown(nav_html, unsafe_allow_html=True)

# Top header
st.markdown("""
<div style="background: linear-gradient(135deg,#fb923c 0%,#f59e0b 55%,#fbbf24 100%); padding: 1.35rem 1.6rem; border-radius: 10px; margin-bottom: 1.2rem; display: flex; align-items: center; justify-content: space-between; box-shadow: 0 10px 24px rgba(249, 115, 22, 0.16); border: 1px solid rgba(255,255,255,0.22);">
<div style="display: flex; align-items: center; gap: 14px;">
<div style="width: 50px; height: 50px; background: rgba(255,255,255,0.15); border: 1px solid rgba(255,255,255,0.22); border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 1.45rem;">
☀️
</div>
<div>
<div style="font-size: 1.55rem; font-weight: 800; color: white; line-height: 1.1; letter-spacing: -0.02em; margin-bottom: 0.25rem;">
UVsense
</div>
<div style="font-size: 0.95rem; color: rgba(255,255,255,0.92); font-weight: 500;">
Smart UV Safety Platform for Young Australians
</div>
</div>
</div>
<div style="display: flex; align-items: center; gap: 0.45rem; background: rgba(255,255,255,0.12); border: 1px solid rgba(255,255,255,0.2); color: white; padding: 0.52rem 0.82rem; border-radius: 999px; font-size: 0.84rem; font-weight: 600; white-space: nowrap; backdrop-filter: blur(6px);">
<span style="width: 8px; height: 8px; border-radius: 50%; background: #86efac; display: inline-block;"></span>
Melbourne, Australia
</div>
</div>
""", unsafe_allow_html=True)

# Top nav
render_top_nav(st.session_state.page)

st.markdown("<div style='margin-bottom: 1.5rem;'></div>", unsafe_allow_html=True)

page = st.session_state.page

if page == "dashboard":
    from views import home
    home.render()
elif page == "uv-awareness":
    from views import uv_awareness
    uv_awareness.render()
elif page == "skin-type-tool":
    from views import skin_type_tool
    skin_type_tool.render()
elif page == "protection-planner":
    from views import protection_planner
    protection_planner.render()
elif page == "reminder-settings":
    from views import reminder_settings
    reminder_settings.render()