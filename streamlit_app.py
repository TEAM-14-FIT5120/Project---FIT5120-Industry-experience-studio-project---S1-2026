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
        border: 4px solid #ef4444;
        border-radius: 50%;
        width: 200px;
        height: 200px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin: 2rem auto;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }

    .uv-number {
        font-size: 10rem;
        font-weight: 700;
        color: #ef4444;
        margin: 0;
    }

    .uv-label {
        font-size: 0.875rem;
        color: #6b7280;
        margin: 0;
    }

    .uv-level {
        font-size: 1.25rem;
        font-weight: 600;
        color: #ef4444;
        margin: 0.5rem 0 0 0;
    }

    .warning-banner {
        background: #ef4444;
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

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    [data-testid="stSidebar"] {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

# Session state
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

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
nav1, nav2, nav3, nav4, nav5 = st.columns(5)

with nav1:
    if st.button("🏠 Dashboard", use_container_width=True):
        st.session_state.page = "Dashboard"

with nav2:
    if st.button("📊 UV Awareness", use_container_width=True):
        st.session_state.page = "UV Awareness"

with nav3:
    if st.button("👤 Skin Type Tool", use_container_width=True):
        st.session_state.page = "Skin Type Tool"

with nav4:
    if st.button("📅 Protection Planner", use_container_width=True):
        st.session_state.page = "Protection Planner"

with nav5:
    if st.button("🔔 Reminder Settings", use_container_width=True):
        st.session_state.page = "Reminder Settings"

st.markdown("<div style='margin-bottom: 1.5rem;'></div>", unsafe_allow_html=True)

page = st.session_state.page

# Render page
if page == "Dashboard":
    from views import home
    home.render()
elif page == "UV Awareness":
    from views import uv_awareness
    uv_awareness.render()
elif page == "Skin Type Tool":
    from views import skin_type_tool
    skin_type_tool.render()
elif page == "Protection Planner":
    from views import protection_planner
    protection_planner.render()
elif page == "Reminder Settings":
    from views import reminder_settings
    reminder_settings.render()