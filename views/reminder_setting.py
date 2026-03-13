"""
UV Alert Preferences - Configure local browser-based UV alerts
"""

import streamlit as st
from datetime import time


def render():
    st.title("UV Alert Preferences")
    st.markdown("""
    <p style='font-size: 1.125rem; color: #6b7280; margin-bottom: 3rem;'>
        Personalize your UV alerts and sunscreen reminder preferences for this browser session.
        No login or account is required.
    </p>
    """, unsafe_allow_html=True)

    # Master toggle
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("### 🔔 Enable UV Alerts")
        st.markdown(
            "<p style='color: #6b7280; margin: 0;'>Show in-app UV alerts and sunscreen reminder prompts while using the website</p>",
            unsafe_allow_html=True
        )
    with col2:
        master_toggle = st.toggle("Enable alerts", value=True, key="master_toggle")

    st.markdown("</div>", unsafe_allow_html=True)

    if master_toggle:
        st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)

        # Morning reminder
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("### ☀️ Morning UV Summary")

        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("Show a morning UV summary on the website dashboard")
            morning_time = st.time_input(
                "Preferred summary time",
                value=time(8, 0),
                key="morning_time",
                help="Choose when you would like to view your morning UV summary."
            )
        with col2:
            morning_enabled = st.toggle("Enable summary", value=True, key="morning_enabled")

        if morning_enabled:
            st.success(f"✅ Morning UV summary set for {morning_time.strftime('%I:%M %p')}")

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div style='margin: 1.5rem 0;'></div>", unsafe_allow_html=True)
