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

    def divider():
        st.markdown("""
        <div style="
        height: 1px;
        background: linear-gradient(to right, transparent, #e5e7eb, transparent);
        margin: 1.2rem 0;
        "></div>
        """, unsafe_allow_html=True)

    saved = st.session_state.get("uv_alert_preferences_saved", {})

    default_alerts_enabled = saved.get("alerts_enabled", True)
    default_reapply_interval = saved.get("reapply_interval", 2)
    default_start_time = time.fromisoformat(saved.get("start_time", "10:00:00"))
    default_end_time = time.fromisoformat(saved.get("end_time", "16:00:00"))
    default_uv_threshold = saved.get("uv_threshold", 8)

    st.markdown("### 🔔 Enable Reminders")
    alerts_enabled = st.toggle(
        "Turn on reminders",
        value=default_alerts_enabled,
        key="alerts_enabled"
    )

    reapply_interval = default_reapply_interval
    start_time = default_start_time
    end_time = default_end_time
    uv_threshold = default_uv_threshold
    active_hours_valid = True

    if alerts_enabled:
        divider()

        st.markdown("### 🧴 Sunscreen Reapplication")
        interval_options = [1, 1.5, 2, 2.5, 3]
        interval_index = interval_options.index(default_reapply_interval) if default_reapply_interval in interval_options else 2

        reapply_interval = st.selectbox(
            "Reminder interval",
            options=interval_options,
            index=interval_index,
            format_func=lambda x: f"Every {x} hours",
            key="reapply_interval"
        )

        divider()

        st.markdown("### ⏰ Outdoor Hours")
        col1, col2 = st.columns(2)

        with col1:
            start_time = st.time_input(
                "Start time",
                value=default_start_time,
                key="start_time"
            )

        with col2:
            end_time = st.time_input(
                "End time",
                value=default_end_time,
                key="end_time"
            )

        active_hours_valid = start_time < end_time
        if not active_hours_valid:
            st.error("Start time must be earlier than end time.")

        divider()

        st.markdown("### ☀️ High UV Alert")
        threshold_options = [6, 7, 8, 9, 10, 11]
        threshold_index = threshold_options.index(default_uv_threshold) if default_uv_threshold in threshold_options else 2

        uv_threshold = st.selectbox(
            "Alert me when UV reaches",
            options=threshold_options,
            index=threshold_index,
            format_func=lambda x: f"UV Index {x}+",
            key="uv_threshold"
        )

    else:
        st.info("Reminders are currently turned off.")

    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)

    if st.button("💾 Save Settings", use_container_width=True, type="primary"):
        if alerts_enabled and not active_hours_valid:
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