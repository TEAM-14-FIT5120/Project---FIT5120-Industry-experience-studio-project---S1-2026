"""
Protection Planner - Daily sun protection planning tool
Uses real UV data from OpenWeather hourly forecast.
"""

import streamlit as st
from datetime import datetime, time, timedelta
import plotly.graph_objects as go
from views.get_live_uv import get_weather_data


def get_uv_color(uv):
    if uv <= 2:
        return "#22c55e"
    elif uv <= 5:
        return "#facc15"
    elif uv <= 7:
        return "#f97316"
    elif uv <= 10:
        return "#ef4444"
    return "#a855f7"


def render():
    st.title("Protection Planner")
    st.markdown("""
    <p style='font-size: 1.125rem; color: #6b7280; margin-bottom: 1.25rem;'>
        Plan your outdoor activities and get personalized sun protection schedules based on the live UV forecast.
    </p>
    """, unsafe_allow_html=True)

    st.markdown("### 📅 Plan Your Outdoor Activity")

    col1, col2 = st.columns(2)

    with col1:
        activity_date = st.date_input(
            "Activity Date",
            value=datetime.now().date(),
            min_value=datetime.now().date()
        )

        activity_type = st.selectbox(
            "Activity Type",
            [
                "Beach/Swimming",
                "Outdoor Sports",
                "Hiking",
                "Picnic/BBQ",
                "Gardening",
                "Walking/Running",
                "Cycling",
                "Other"
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

    st.markdown("<div style='margin: 0.75rem 0;'></div>", unsafe_allow_html=True)

    if st.button("🌞 Generate Protection Plan", use_container_width=True):
        start_datetime = datetime.combine(activity_date, start_time)
        end_datetime = start_datetime + timedelta(hours=duration)

        try:
            weather_data = get_weather_data(location.strip() if location.strip() else None)

            if not weather_data:
                st.error("Could not fetch UV data for this location.")
                return

            current_uv = weather_data.get("current", {}).get("uvi", 0)
            city_name = weather_data.get("display_location", location if location else "Current Location")
            timezone_offset = weather_data.get("timezone_offset", 0)
            hourly_data = weather_data.get("hourly", [])
            location_error = weather_data.get("location_error")

            if location_error:
                st.warning(f"Using default location because: {location_error}")

            if not hourly_data:
                st.error("Hourly UV forecast is not available.")
                return

            hours = []
            uv_values = []

            for hour in hourly_data[:24]:
                hour_ts = hour.get("dt")
                hour_uv = hour.get("uvi", 0)

                if hour_ts is None:
                    continue

                # Convert API UTC timestamp to location local time
                local_hour_dt = datetime.utcfromtimestamp(hour_ts + timezone_offset)

                if start_datetime <= local_hour_dt <= end_datetime:
                    hours.append(local_hour_dt.strftime("%I:%M %p"))
                    uv_values.append(round(hour_uv, 1))

            if not hours:
                st.warning("No hourly UV forecast found for the selected activity time.")
                return

        except Exception as e:
            st.error(f"Unable to load live UV data: {e}")
            return

        st.markdown(
            f"""
            <div style='background: #eff6ff; border-left: 4px solid #3b82f6;
                 padding: 1rem; margin: 0.75rem 0 1rem 0; border-radius: 8px;'>
                <strong>Live UV forecast loaded</strong><br>
                Location: {city_name}<br>
                Current UV: <strong>{current_uv}</strong>
            </div>
            """,
            unsafe_allow_html=True
        )

        # UV forecast chart
        st.markdown("### ☀️ UV Index Forecast")

        colors = [get_uv_color(uv) for uv in uv_values]

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=hours,
            y=uv_values,
            marker_color=colors,
            text=uv_values,
            textposition="outside",
            hovertemplate="<b>%{x}</b><br>UV Index: %{y}<extra></extra>"
        ))

        fig.update_layout(
            height=350,
            margin=dict(l=20, r=20, t=20, b=80),
            plot_bgcolor="white",
            paper_bgcolor="white",
            xaxis=dict(
                title="Time",
                showgrid=False,
                linecolor="#e5e7eb",
                tickangle=-45
            ),
            yaxis=dict(
                title="UV Index",
                showgrid=True,
                gridcolor="#f3f4f6",
                linecolor="#e5e7eb",
                range=[0, max(uv_values) + 2]
            ),
            showlegend=False
        )

        st.plotly_chart(fig, use_container_width=True)

        max_uv = max(uv_values)
        peak_time = hours[uv_values.index(max_uv)]

        if max_uv >= 8:
            st.error(f"⚠️ **High UV Alert:** Peak UV of {max_uv} expected at {peak_time}. Extra protection required!")
        elif max_uv >= 6:
            st.warning(f"⚠️ **Moderate UV Alert:** Peak UV of {max_uv} expected at {peak_time}. Protection recommended.")
        else:
            st.success(f"✅ **Low UV:** Peak UV of {max_uv} at {peak_time}. Standard protection sufficient.")

        # Protection schedule
        st.markdown("<div style='margin: 1rem 0 0.5rem 0;'></div>", unsafe_allow_html=True)
        st.markdown("### 🛡️ Your Protection Schedule")

        st.markdown("**Before You Go:**")
        st.markdown(f"""
        <div style='background: #f0fdf4; border-left: 3px solid #22c55e;
             padding: 1rem; margin: 0.75rem 0; border-radius: 8px;'>
            <strong>{(start_datetime - timedelta(minutes=30)).strftime("%I:%M %p")}</strong> -
            Apply sunscreen 30 minutes before going outside
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='margin: 0.5rem 0;'></div>", unsafe_allow_html=True)
        st.markdown("**During Your Activity:**")

        reapply_times = []
        reapply_interval = timedelta(hours=2)
        next_reapply = start_datetime + reapply_interval

        while next_reapply < end_datetime:
            reapply_times.append(next_reapply)
            next_reapply += reapply_interval

        if reapply_times:
            for idx, reapply_time in enumerate(reapply_times, 1):
                st.markdown(f"""
                <div style='background: #fef3c7; border-left: 3px solid #f59e0b;
                     padding: 1rem; margin: 0.5rem 0; border-radius: 8px;'>
                    <strong>{reapply_time.strftime("%I:%M %p")}</strong> -
                    Reapply sunscreen (Application #{idx + 1})
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No sunscreen reapplication is needed for this short activity duration.")

        st.markdown("<div style='margin: 0.75rem 0;'></div>", unsafe_allow_html=True)
        st.markdown("**Activity-Specific Tips:**")

        activity_tips = {
            "Beach/Swimming": [
                "💧 Use water-resistant SPF 50+ sunscreen",
                "🏊 Reapply immediately after swimming",
                "🏖️ Use beach umbrella during peak hours",
                "👙 Consider rash guard or swim shirt"
            ],
            "Outdoor Sports": [
                "💦 Reapply after sweating heavily",
                "👕 Wear moisture-wicking UV-protective clothing",
                "🧢 Choose a sports cap with neck flap",
                "💧 Stay hydrated to prevent heat stress"
            ],
            "Hiking": [
                "🎒 Pack sunscreen in your bag",
                "👒 Wear wide-brimmed hiking hat",
                "🧥 Long sleeves protect better at altitude",
                "⏰ Take shade breaks every hour"
            ]
        }

        default_tips = [
            "🧴 Keep sunscreen with you",
            "👒 Wear protective clothing",
            "🌳 Take regular shade breaks",
            "💧 Stay hydrated"
        ]

        tips = activity_tips.get(activity_type, default_tips)

        for tip in tips:
            st.markdown(f"""
            <div style='background: #f9fafb; padding: 0.75rem 1rem;
                 margin: 0.5rem 0; border-radius: 8px;'>
                {tip}
            </div>
            """, unsafe_allow_html=True)

        # Packing checklist
        st.markdown("<div style='margin: 1rem 0 0.5rem 0;'></div>", unsafe_allow_html=True)
        st.markdown("### 🎒 Sun Protection Checklist")

        col1, col2 = st.columns(2)

        with col1:
            st.checkbox("SPF 30+ Sunscreen", value=False)
            st.checkbox("Wide-brimmed hat", value=False)
            st.checkbox("UV-protective sunglasses", value=False)
            st.checkbox("Protective clothing", value=False)

        with col2:
            st.checkbox("Water bottle", value=False)
            st.checkbox("Shade equipment (umbrella/tent)", value=False)
            st.checkbox("Lip balm with SPF", value=False)
            st.checkbox("After-sun lotion", value=False)

        st.markdown("<div style='margin: 1rem 0;'></div>", unsafe_allow_html=True)
        st.success("💾 **Tip:** Save this plan or set reminders on your phone!")

    # Quick tips
    st.markdown("<div style='margin: 1.5rem 0 1rem 0;'></div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class='card' style='text-align: center;'>
            <div style='font-size: 3rem; margin-bottom: 1rem;'>🌅</div>
            <h4>Best Times</h4>
            <p style='color: #6b7280; font-size: 0.875rem;'>
                Before 10am and after 4pm usually have lower UV levels
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='card' style='text-align: center;'>
            <div style='font-size: 3rem; margin-bottom: 1rem;'>⏰</div>
            <h4>Reapply Often</h4>
            <p style='color: #6b7280; font-size: 0.875rem;'>
                Every 2 hours, or immediately after swimming or sweating
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class='card' style='text-align: center;'>
            <div style='font-size: 3rem; margin-bottom: 1rem;'>☁️</div>
            <h4>Cloudy Days Too</h4>
            <p style='color: #6b7280; font-size: 0.875rem;'>
                UV can still be high even when the sky looks cloudy
            </p>
        </div>
        """, unsafe_allow_html=True)