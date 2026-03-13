"""
Protection Planner - Daily sun protection planning tool
"""

import streamlit as st
from datetime import datetime, time


def render():
    st.title("Protection Planner")
    st.markdown("""
    <p style='font-size: 1.125rem; color: #6b7280; margin-bottom: 3rem;'>
        Plan your outdoor activities and get personalized sun protection schedules based on the UV forecast.
    </p>
    """, unsafe_allow_html=True)

    # Activity Planning Section
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### 📅 Plan Your Outdoor Activity")

    col1, col2 = st.columns(2)

    with col1:
        activity_date = st.date_input(
            "Activity Date",
            value=datetime.now(),
            min_value=datetime.now()
        )

        activity_type = st.selectbox(
            "Activity Type",
            [
                "Beach/Swimming", "Outdoor Sports", "Hiking", "Picnic/BBQ",
                "Gardening", "Walking/Running", "Cycling", "Other"
            ]
        )

    with col2:
        start_time = st.time_input(
            "Start Time",
            value=time(10, 0)
        )

        duration = st.slider(
            "Duration (hours)",
            min_value=0.5,
            max_value=8.0,
            value=2.0,
            step=0.5
        )

    location = st.text_input(
        "Location (optional)",
        placeholder="e.g., Bondi Beach, Melbourne CBD"
    )

    st.markdown("</div>", unsafe_allow_html=True)