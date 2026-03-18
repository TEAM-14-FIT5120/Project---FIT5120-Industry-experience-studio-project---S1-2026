"""
Protection Planner - Daily sun protection planning tool
"""

import streamlit as st
from datetime import datetime, time, timedelta
import plotly.graph_objects as go


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

    st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)

    # Generate plan button
    if st.button("🌞 Generate Protection Plan", use_container_width=True):
        start_datetime = datetime.combine(activity_date, start_time)
        end_datetime = start_datetime + timedelta(hours=duration)

        hours = []
        uv_values = []
        current_time = start_datetime

        while current_time <= end_datetime:
            hours.append(current_time.strftime("%I:%M %p"))
            hour_of_day = current_time.hour

            if 6 <= hour_of_day <= 18:
                base_uv = 8
                peak_hour = 12
                distance_from_peak = abs(hour_of_day - peak_hour)
                uv = max(2, base_uv - (distance_from_peak * 0.8))
            else:
                uv = 0

            uv_values.append(round(uv, 1))
            current_time += timedelta(hours=0.5)

        # Display UV forecast
        st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("### ☀️ UV Index Forecast")

        fig = go.Figure()

        colors = []
        for uv in uv_values:
            if uv <= 2:
                colors.append('#22c55e')
            elif uv <= 5:
                colors.append('#facc15')
            elif uv <= 7:
                colors.append('#f97316')
            elif uv <= 10:
                colors.append('#ef4444')
            else:
                colors.append('#a855f7')

        fig.add_trace(go.Bar(
            x=hours,
            y=uv_values,
            marker_color=colors,
            text=uv_values,
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>UV Index: %{y}<extra></extra>'
        ))

        fig.update_layout(
            height=350,
            margin=dict(l=20, r=20, t=20, b=80),
            plot_bgcolor='white',
            paper_bgcolor='white',
            xaxis=dict(
                title='Time',
                showgrid=False,
                linecolor='#e5e7eb',
                tickangle=-45
            ),
            yaxis=dict(
                title='UV Index',
                showgrid=True,
                gridcolor='#f3f4f6',
                linecolor='#e5e7eb',
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

        st.markdown("</div>", unsafe_allow_html=True)

        # Protection recommendations
        st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("### 🛡️ Your Protection Schedule")

        reapply_times = []

        st.markdown("**Before You Go:**")
        st.markdown(f"""
        <div style='background: #f0fdf4; border-left: 3px solid #22c55e;
             padding: 1rem; margin: 1rem 0; border-radius: 4px;'>
            <strong>{(start_datetime - timedelta(minutes=30)).strftime("%I:%M %p")}</strong> -
            Apply sunscreen 30 minutes before going outside
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='margin: 1.5rem 0;'></div>", unsafe_allow_html=True)
        st.markdown("**During Your Activity:**")

        reapply_interval = timedelta(hours=2)
        next_reapply = start_datetime + reapply_interval

        while next_reapply < end_datetime:
            reapply_times.append(next_reapply)
            next_reapply += reapply_interval

        for idx, reapply_time in enumerate(reapply_times, 1):
            st.markdown(f"""
            <div style='background: #fef3c7; border-left: 3px solid #f59e0b;
                 padding: 1rem; margin: 0.5rem 0; border-radius: 4px;'>
                <strong>{reapply_time.strftime("%I:%M %p")}</strong> -
                Reapply sunscreen (Application #{idx + 1})
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='margin: 1.5rem 0;'></div>", unsafe_allow_html=True)
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

        st.markdown("</div>", unsafe_allow_html=True)

        # Packing checklist
        st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("### 🎒 Sun Protection Checklist")

        col1, col2 = st.columns(2)

        with col1:
            st.checkbox("✅ SPF 30+ Sunscreen", value=False)
            st.checkbox("✅ Wide-brimmed hat", value=False)
            st.checkbox("✅ UV-protective sunglasses", value=False)
            st.checkbox("✅ Protective clothing", value=False)

        with col2:
            st.checkbox("✅ Water bottle", value=False)
            st.checkbox("✅ Shade equipment (umbrella/tent)", value=False)
            st.checkbox("✅ Lip balm with SPF", value=False)
            st.checkbox("✅ After-sun lotion", value=False)

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)

        st.success("💾 **Tip:** Save this plan or set reminders on your phone!")

    # Quick tips section
    st.markdown("<div style='margin: 3rem 0;'></div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class='card' style='text-align: center;'>
            <div style='font-size: 3rem; margin-bottom: 1rem;'>🌅</div>
            <h4>Best Times</h4>
            <p style='color: #6b7280; font-size: 0.875rem;'>
                Before 10am and after 4pm have lower UV levels
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='card' style='text-align: center;'>
            <div style='font-size: 3rem; margin-bottom: 1rem;'>⏰</div>
            <h4>Reapply Often</h4>
            <p style='color: #6b7280; font-size: 0.875rem;'>
                Every 2 hours, or immediately after swimming/sweating
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class='card' style='text-align: center;'>
            <div style='font-size: 3rem; margin-bottom: 1rem;'>☁️</div>
            <h4>Cloudy Days Too</h4>
            <p style='color: #6b7280; font-size: 0.875rem;'>
                Up to 80% of UV rays penetrate clouds
            </p>
        </div>
        """, unsafe_allow_html=True)