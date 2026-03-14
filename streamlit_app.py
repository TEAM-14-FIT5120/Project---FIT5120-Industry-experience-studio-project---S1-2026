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
        background: linear-gradient(135deg, #fff5f0 0%, #fffbea 50%, #eff6ff 100%);
    }

    .stButton > button {
        background: white;
        color: #1f2937;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 0.7rem 1rem;
        font-weight: 600;
        min-height: 48px;
        width: 100%;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }

    .stButton > button:hover {
        border-color: #fb923c;
        color: #ea580c;
    }

    .card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
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
        padding: 1rem;
        border-radius: 12px;
        text-align: center;
        margin: 1.5rem auto;
        max-width: 700px;
        font-weight: 500;
    }

    .protection-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        text-align: center;
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
    gap: 0.75rem;
    margin-bottom: 1.5rem;
    flex-wrap: wrap;
    }

    .nav-item {
        flex: 1;
        min-width: 160px;
        display: block;
        text-decoration: none;
        text-align: center;
        background: white;
        color: #1f2937 !important;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 0.8rem 1rem;
        font-weight: 600;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        transition: all 0.2s ease;
    }

    .nav-item:hover {
        border-color: #fb923c;
        color: #ea580c !important;
        transform: translateY(-1px);
    }

    .nav-item.active {
        background: linear-gradient(90deg, #fb923c 0%, #fbbf24 100%);
        color: white !important;
        border: 1px solid #fb923c;
        box-shadow: 0 4px 12px rgba(251, 146, 60, 0.28);
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
        ("dashboard", "🏠 Dashboard"),
        ("uv-awareness", "📊 UV Awareness"),
        ("skin-type-tool", "👤 Skin Type Tool"),
        ("protection-planner", "📅 Protection Planner"),
        ("reminder-settings", "🔔 Reminder Settings"),
    ]

    nav_html = "<div class='navbar'>"

    for slug, label in nav_items:
        active_class = "active" if current_page == slug else ""
        nav_html += f"""<a class="nav-item {active_class}" href="?page={slug}" target="_self">{label}</a>"""

    nav_html += "</div>"

    st.markdown(nav_html, unsafe_allow_html=True)

# Top header
st.markdown("""
<div style='background: linear-gradient(90deg, #fb923c 0%, #fbbf24 100%);
            padding: 1rem 1.5rem; border-radius: 14px; margin-bottom: 1rem;
            display: flex; align-items: center; justify-content: space-between;'>
    <div style='display: flex; align-items: center; gap: 12px;'>
        <div style='width: 44px; height: 44px; background: rgba(255,255,255,0.25);
                    border-radius: 50%; display: flex; align-items: center; justify-content: center;
                    font-size: 1.4rem;'>
            ☀️
        </div>
        <div>
            <div style='font-size: 1.35rem; font-weight: 700; color: white;'>UVsense</div>
            <div style='font-size: 0.9rem; color: rgba(255,255,255,0.9);'>
                UV Safety Platform · Melbourne, Australia
            </div>
        </div>
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