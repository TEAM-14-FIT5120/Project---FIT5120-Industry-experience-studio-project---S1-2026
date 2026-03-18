"""
Reminder Settings - Configure browser-based UV reminders
"""

import streamlit as st
from datetime import time


def render():
    st.title("Reminder Settings")
    st.markdown(
        """
        <p style='font-size: 1rem; color: #6b7280; margin-bottom: 0.5rem;'>
            Set your UV and sunscreen reminders for this browser session.
        </p>
        """,
        unsafe_allow_html=True
    )

    # 👉 分割线函数（统一风格）
    def divider():
        st.markdown("""
        <div style="
        height: 1px;
        background: linear-gradient(to right, transparent, #e5e7eb, transparent);
        margin: 1.2rem 0;
        "></div>
        """, unsafe_allow_html=True)

    # Enable reminders
    st.markdown("### 🔔 Enable Reminders")
    alerts_enabled = st.toggle("Turn on reminders", value=True, key="alerts_enabled")

    if alerts_enabled:

        divider()

        # Sunscreen reminder
        st.markdown("### 🧴 Sunscreen Reapplication")
        reapply_interval = st.selectbox(
            "Reminder interval",
            options=[1, 1.5, 2, 2.5, 3],
            index=2,
            format_func=lambda x: f"Every {x} hours",
            key="reapply_interval"
        )

        divider()

        # Outdoor hours
        st.markdown("### ⏰ Outdoor Hours")
        col1, col2 = st.columns(2)
        with col1:
            start_time = st.time_input(
                "Start time",
                value=time(10, 0),
                key="start_time"
            )
        with col2:
            end_time = st.time_input(
                "End time",
                value=time(16, 0),
                key="end_time"
            )

        active_hours_valid = start_time < end_time
        if not active_hours_valid:
            st.error("Start time must be earlier than end time.")

        divider()

        # UV threshold
        st.markdown("### ☀️ High UV Alert")
        uv_threshold = st.selectbox(
            "Alert me when UV reaches",
            options=[6, 7, 8, 9, 10, 11],
            index=2,
            format_func=lambda x: f"UV Index {x}+",
            key="uv_threshold"
        )

        st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)

        if st.button("💾 Save Settings", use_container_width=True, type="primary"):
            if not active_hours_valid:
                st.error("Please fix the time settings before saving.")
            else:
                st.session_state["uv_alert_preferences_saved"] = {
                    "alerts_enabled": alerts_enabled,
                    "reapply_interval": reapply_interval,
                    "start_time": str(start_time),
                    "end_time": str(end_time),
                    "uv_threshold": uv_threshold
                }
                st.success("Your reminder settings have been saved.")

    else:
        st.info("Reminders are currently turned off.")