from datetime import datetime


def get_simulated_uv_reminders(current_uv, preferences, session_state):
    """
    Simulate in-app UV reminders based on:
    - current UV level
    - saved user preferences
    - current local time

    Uses session_state to avoid duplicate reminders in the same period.
    """

    if not preferences or not preferences.get("alerts_enabled", False):
        return []

    reminders = []

    reapply_interval = float(preferences.get("reapply_interval", 2))
    start_time_str = preferences.get("start_time", "10:00:00")
    end_time_str = preferences.get("end_time", "16:00:00")
    uv_threshold = int(preferences.get("uv_threshold", 8))

    now = datetime.now()
    today_str = now.strftime("%Y-%m-%d")

    start_dt = datetime.combine(
        now.date(),
        datetime.strptime(start_time_str, "%H:%M:%S").time()
    )
    end_dt = datetime.combine(
        now.date(),
        datetime.strptime(end_time_str, "%H:%M:%S").time()
    )

    # Reset tracking each day
    if session_state.get("last_reminder_date") != today_str:
        session_state["last_reminder_date"] = today_str
        session_state["last_reapply_slot"] = -1
        session_state["last_uv_alert_shown"] = False

    # 1. High UV alert
    if current_uv >= uv_threshold:
        if not session_state.get("last_uv_alert_shown", False):
            reminders.append({
                "type": "uv",
                "title": "High UV Alert",
                "message": f"UV index is now {current_uv}. Apply sunscreen, wear a hat, and seek shade where possible."
            })
            session_state["last_uv_alert_shown"] = True
    else:
        session_state["last_uv_alert_shown"] = False

    # 2. Sunscreen reapplication reminder
    if start_dt <= now <= end_dt:
        elapsed_hours = (now - start_dt).total_seconds() / 3600
        current_slot = int(elapsed_hours // reapply_interval)

        if current_slot >= 1 and current_slot > session_state.get("last_reapply_slot", -1):
            reminders.append({
                "type": "reapply",
                "title": "Sunscreen Reminder",
                "message": f"It has been about {reapply_interval} hours since your outdoor start time. Consider reapplying sunscreen."
            })
            session_state["last_reapply_slot"] = current_slot

    return reminders


def render_reminder_card(title, message, icon="🔔", bg="#fff7ed", border="#fdba74"):
    """
    Render a custom reminder card in Streamlit.
    """
    import streamlit as st

    st.markdown(
        f"""
        <div style="
            background: {bg};
            border: 1px solid {border};
            border-radius: 16px;
            padding: 1rem 1.2rem;
            margin: 1rem 0;
            box-shadow: 0 4px 14px rgba(0,0,0,0.05);
        ">
            <div style="
                font-size: 1rem;
                font-weight: 700;
                color: #111827;
                margin-bottom: 0.35rem;
            ">
                {icon} {title}
            </div>
            <div style="
                color: #4b5563;
                font-size: 0.96rem;
                line-height: 1.5;
            ">
                {message}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )