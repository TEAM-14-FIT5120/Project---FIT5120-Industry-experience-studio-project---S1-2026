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

        # Sunscreen application reminders
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("### 🧴 Sunscreen Reapplication Prompts")

        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("Show sunscreen reapplication prompts during your selected outdoor hours")
            reapply_interval = st.select_slider(
                "Prompt interval",
                options=[1, 1.5, 2, 2.5, 3],
                value=2,
                format_func=lambda x: f"Every {x} hours",
                key="reapply_interval"
            )
        with col2:
            reapply_enabled = st.toggle("Enable prompts", value=True, key="reapply_enabled")

        if reapply_enabled:
            st.info(f"ℹ️ In-app prompts will appear every {reapply_interval} hours during your active hours")

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div style='margin: 1.5rem 0;'></div>", unsafe_allow_html=True)

        # Active hours
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("### ⏰ Outdoor Active Hours")
        st.markdown(
            "<p style='color: #6b7280;'>Choose the time period when you are usually outdoors</p>",
            unsafe_allow_html=True
        )

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

        if active_hours_valid:
            st.success(f"✅ Active hours: {start_time.strftime('%I:%M %p')} - {end_time.strftime('%I:%M %p')}")
        else:
            st.error("Start time must be earlier than end time.")

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div style='margin: 1.5rem 0;'></div>", unsafe_allow_html=True)

        # UV threshold alerts
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("### ⚠️ High UV Alerts")

        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("Show an alert when the UV index reaches your selected risk level")
            uv_threshold = st.select_slider(
                "Alert threshold",
                options=[6, 7, 8, 9, 10, 11],
                value=8,
                format_func=lambda x: f"UV Index {x}+",
                key="uv_threshold"
            )
        with col2:
            uv_alert_enabled = st.toggle("Enable alert", value=True, key="uv_alert_enabled")

        if uv_alert_enabled:
            threshold_label = "High" if uv_threshold < 8 else "Very High" if uv_threshold < 11 else "Extreme"
            st.warning(f"⚠️ Alerts will appear when UV reaches {threshold_label} levels (UV {uv_threshold}+).")

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div style='margin: 1.5rem 0;'></div>", unsafe_allow_html=True)

        # Activity-based reminders
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("### 🏃 Activity-Based Prompts")
        st.markdown(
            "<p style='color: #6b7280;'>Set a prompt before planned outdoor activities</p>",
            unsafe_allow_html=True
        )

        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("**Prompt before outdoor activities**")
            before_activity = st.number_input(
                "Minutes before activity",
                min_value=5,
                max_value=60,
                value=30,
                step=5,
                key="before_activity"
            )
        with col2:
            st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
            activity_reminder_enabled = st.toggle("Enable prompt", value=True, key="activity_reminder")

        if activity_reminder_enabled:
            st.info(f"ℹ️ A prompt will appear {before_activity} minutes before your planned outdoor activity")

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div style='margin: 1.5rem 0;'></div>", unsafe_allow_html=True)

        # Days active
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("### 📅 Active Days")
        st.markdown(
            "<p style='color: #6b7280;'>Choose which days you want alerts and prompts to appear</p>",
            unsafe_allow_html=True
        )

        col1, col2, col3 = st.columns(3)

        days_enabled = {}

        with col1:
            days_enabled["Monday"] = st.checkbox("Monday", value=True, key="day_monday")
            days_enabled["Tuesday"] = st.checkbox("Tuesday", value=True, key="day_tuesday")
            days_enabled["Wednesday"] = st.checkbox("Wednesday", value=True, key="day_wednesday")

        with col2:
            days_enabled["Thursday"] = st.checkbox("Thursday", value=True, key="day_thursday")
            days_enabled["Friday"] = st.checkbox("Friday", value=True, key="day_friday")
            days_enabled["Saturday"] = st.checkbox("Saturday", value=True, key="day_saturday")

        with col3:
            days_enabled["Sunday"] = st.checkbox("Sunday", value=True, key="day_sunday")

        active_days = [day for day, enabled in days_enabled.items() if enabled]

        if active_days:
            st.success(f"✅ Alerts active on: {', '.join(active_days)}")
        else:
            st.warning("⚠️ No active days selected. Please choose at least one day.")

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div style='margin: 1.5rem 0;'></div>", unsafe_allow_html=True)

        # Display preferences
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("### 📱 Alert Display Preferences")

        display_method = st.multiselect(
            "How would you like alerts to appear on the website?",
            ["Dashboard card", "Banner alert", "Reminder prompt"],
            default=["Dashboard card", "Reminder prompt"],
            key="display_method"
        )

        if display_method:
            st.success(f"✅ Alerts will appear as: {', '.join(display_method)}")
        else:
            st.warning("⚠️ Please select at least one display method.")

        st.markdown("<div style='margin: 1rem 0;'></div>", unsafe_allow_html=True)

        highlight_alerts = st.checkbox("Highlight high UV alerts visually", value=True, key="highlight_alerts")
        show_icons = st.checkbox("Show icons in alerts", value=True, key="show_icons")

        st.markdown("</div>", unsafe_allow_html=True)

        # Save button
        st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)

        validation_errors = []

        if not active_hours_valid:
            validation_errors.append("Active hours are invalid.")
        if not active_days:
            validation_errors.append("At least one active day must be selected.")
        if not display_method:
            validation_errors.append("At least one alert display method must be selected.")

        if st.button("💾 Save Preferences", use_container_width=True, type="primary"):
            if validation_errors:
                st.error("Please fix the following before saving:")
                for err in validation_errors:
                    st.markdown(f"- {err}")
            else:
                st.session_state["uv_alert_preferences_saved"] = {
                    "master_toggle": master_toggle,
                    "morning_enabled": morning_enabled,
                    "morning_time": str(morning_time),
                    "reapply_enabled": reapply_enabled,
                    "reapply_interval": reapply_interval,
                    "start_time": str(start_time),
                    "end_time": str(end_time),
                    "uv_alert_enabled": uv_alert_enabled,
                    "uv_threshold": uv_threshold,
                    "activity_reminder_enabled": activity_reminder_enabled,
                    "before_activity": before_activity,
                    "active_days": active_days,
                    "display_method": display_method,
                    "highlight_alerts": highlight_alerts,
                    "show_icons": show_icons
                }

                st.success("✅ Your UV alert preferences have been saved for this browser session.")
                st.balloons()

    else:
        st.info("ℹ️ Enable UV alerts to customize your preferences.")
     # Tips section
    st.markdown("<div style='margin: 3rem 0;'></div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class='card'>
            <h4>💡 Tips</h4>
            <ul style='color: #6b7280; line-height: 1.8;'>
                <li>Set your morning summary before leaving home</li>
                <li>Use 2-hour sunscreen prompts for long outdoor periods</li>
                <li>Turn on high UV alerts for extra awareness</li>
                <li>Adjust active hours based on your daily schedule</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='card'>
            <h4>🖥️ How It Works</h4>
            <p style='color: #6b7280; line-height: 1.8;'>
                These preferences control how UV alerts and reminder prompts appear
                while using this website. Because no login is required, settings are
                kept only for the current browser session.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Privacy note
    st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style='background: #eff6ff; border-left: 4px solid #3b82f6;
         padding: 1rem; border-radius: 4px;'>
        <strong>🔒 Privacy Note:</strong> This page does not require login or account creation.
        Preferences are used only to personalize your experience on this website during use.
    </div>
    """, unsafe_allow_html=True)