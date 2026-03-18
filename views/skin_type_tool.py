"""Skin Type Tool with AI Advisor"""
import streamlit as st
import plotly.graph_objects as go
from views.get_live_uv import get_weather_data

def calculate_burn_time(fitzpatrick_num, uv_index):
    base_times = {1: 67, 2: 100, 3: 133, 4: 200, 5: 300, 6: 400}
    if uv_index <= 0:
        return 999
    return max(1, round(base_times.get(fitzpatrick_num, 133) / uv_index))

def get_uv_color(uv):
    if uv <= 2: return "#22c55e"
    elif uv <= 5: return "#eab308"
    elif uv <= 7: return "#f97316"
    elif uv <= 10: return "#ef4444"
    else: return "#a855f7"

def all_skin_types_chart(current_uv):
    skin_types = ["Type I\n(Very Fair)", "Type II\n(Fair)", "Type III\n(Medium)", "Type IV\n(Olive)", "Type V\n(Brown)", "Type VI\n(Dark)"]
    burn_times = [min(calculate_burn_time(k, current_uv), 120) for k in range(1, 7)]
    bar_colors = ["#dc2626", "#f97316", "#eab308", "#84cc16", "#22c55e", "#10b981"]
    fig = go.Figure(go.Bar(
        x=skin_types, y=burn_times,
        marker_color=bar_colors,
        text=[f"{b} min" for b in burn_times],
        textposition="outside",
        hovertemplate="%{x}<br>Burn time: %{y} min<extra></extra>"
    ))
    fig.update_layout(
        title={"text": f"Burn time for all skin types at UV {current_uv}", "font": {"size": 15, "color": "#1f2937"}, "x": 0},
        xaxis={"showgrid": False, "linecolor": "#e5e7eb"},
        yaxis={"title": "Minutes before skin damage", "showgrid": True, "gridcolor": "#f3f4f6", "range": [0, 130]},
        height=350, margin=dict(l=60, r=20, t=60, b=60),
        paper_bgcolor="white", plot_bgcolor="white", showlegend=False
    )
    return fig

def render():
    st.title("Skin Type Protection Tool")
    st.markdown("<p style='font-size: 1.125rem; color: #6b7280; margin-bottom: 2rem;'>Answer a few questions to get personalized sun protection recommendations based on your skin type.</p>", unsafe_allow_html=True)

    st.markdown("#### 1. What is your natural skin color?")
    skin_color = st.radio("skin_color", ["Very fair or pale", "Fair", "Medium", "Olive or light brown", "Brown or dark brown"], label_visibility="collapsed")
    st.markdown("#### 2. How does your skin react to sun exposure in summer?")
    sun_reaction = st.radio("sun_reaction", ["Always burns, never tans", "Burns easily, tans minimally", "Burns moderately, tans gradually", "Burns minimally, tans easily", "Rarely burns, tans very easily"], label_visibility="collapsed")
    st.markdown("#### 3. What is your natural hair color?")
    hair_color = st.radio("hair_color", ["Red or light blonde", "Blonde", "Light brown", "Dark brown", "Black"], label_visibility="collapsed")
    st.markdown("#### 4. Do you have freckles on unexposed skin?")
    freckles = st.radio("freckles", ["Many", "Several", "Few", "Very few", "None"], label_visibility="collapsed")

    if st.button("Get My Skin Type & Protection Plan", use_container_width=True):
        score = 0
        score += {"Very fair or pale": 0, "Fair": 1, "Medium": 2, "Olive or light brown": 3, "Brown or dark brown": 4}.get(skin_color, 0)
        score += {"Always burns, never tans": 0, "Burns easily, tans minimally": 1, "Burns moderately, tans gradually": 2, "Burns minimally, tans easily": 3, "Rarely burns, tans very easily": 4}.get(sun_reaction, 0)
        if score <= 2:
            st.session_state.update({"skin_type": "Type I", "skin_type_name": "Very Fair", "risk_level": "Extreme Risk", "risk_color": "#dc2626", "fitzpatrick_num": 1,
                "recommendations": ["Apply SPF 50+ sunscreen every 90 minutes", "Always wear a wide-brimmed hat outdoors", "Wear long sleeves and pants when possible", "UV-blocking sunglasses are essential", "Seek shade between 10am-4pm", "Limit sun exposure to less than 30 minutes", "Avoid tanning beds completely"]})
        elif score <= 5:
            st.session_state.update({"skin_type": "Type II", "skin_type_name": "Fair", "risk_level": "High Risk", "risk_color": "#ea580c", "fitzpatrick_num": 2,
                "recommendations": ["Apply SPF 30-50 sunscreen every 2 hours", "Wear a hat when outdoors for extended periods", "Cover up during peak sun hours", "Wear UV-protective sunglasses", "Seek shade during midday hours", "Build up sun exposure gradually", "Use UV index apps to plan activities"]})
        elif score <= 9:
            st.session_state.update({"skin_type": "Type III", "skin_type_name": "Medium", "risk_level": "Moderate Risk", "risk_color": "#f59e0b", "fitzpatrick_num": 3,
                "recommendations": ["Apply SPF 30+ sunscreen every 2-3 hours", "Wear a hat during extended outdoor activities", "Use UV-protective sunglasses", "Take shade breaks during peak hours", "Reapply sunscreen after swimming", "Be extra cautious at beach or pool", "Monitor UV index daily"]})
        elif score <= 13:
            st.session_state.update({"skin_type": "Type IV", "skin_type_name": "Olive", "risk_level": "Moderate Risk", "risk_color": "#f59e0b", "fitzpatrick_num": 4,
                "recommendations": ["Apply SPF 30 sunscreen every 3 hours", "Wear sunglasses for eye protection", "Hat recommended for extended exposure", "Seek shade when UV index is high", "Reapply after swimming or sweating", "Extra protection at beach/snow", "Still vulnerable to UV damage"]})
        else:
            st.session_state.update({"skin_type": "Type V-VI", "skin_type_name": "Dark", "risk_level": "Lower Risk", "risk_color": "#10b981", "fitzpatrick_num": 5,
                "recommendations": ["Apply SPF 15-30 sunscreen daily", "Wear sunglasses for eye protection", "Reapply sunscreen every 3-4 hours", "Extra protection during water activities", "Shade recommended during peak UV", "Still need sun protection", "Check UV index for outdoor planning"]})
        st.session_state["quiz_done"] = True
        st.session_state.pop("ai_advice", None)

    if st.session_state.get("quiz_done"):
        rc = st.session_state.risk_color
        st.markdown(f"<div style='background: linear-gradient(135deg, {rc}20 0%, {rc}10 100%); padding: 2rem; border-radius: 12px; border-left: 4px solid {rc}; margin: 1rem 0;'><h2 style='margin:0 0 0.5rem 0;'>Your Results</h2><p style='font-size: 2rem; font-weight: 700; color: {rc}; margin:0;'>{st.session_state.skin_type} — {st.session_state.skin_type_name}</p><p style='font-size: 1.25rem; color: {rc}; margin:0.25rem 0 0 0;'>{st.session_state.risk_level}</p></div>", unsafe_allow_html=True)
        st.markdown("### Your Protection Recommendations")
        for rec in st.session_state.recommendations:
            st.markdown(f"<div style='background: #f9fafb; padding: 0.75rem 1rem; border-radius: 8px; margin-bottom: 0.5rem; border-left: 3px solid {rc};'>{rec}</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### ✨ AI Protection Advisor")
        st.caption("Get a personalised plan based on your skin type and today's live UV index in Melbourne.")

        if st.button("✨ Generate My AI Protection Plan", use_container_width=True, key="ai_btn"):
            _st = st.session_state.skin_type
            _stn = st.session_state.skin_type_name
            _rl = st.session_state.risk_level
            _fn = st.session_state.fitzpatrick_num
            # Use cached UV if available to avoid geolocation reset
            if "cached_uv" not in st.session_state:
                with st.spinner("Fetching live UV data..."):
                    wd = get_weather_data()
                    st.session_state["cached_uv"] = round(wd.get("current", {}).get("uvi", 6)) if wd else 6
            uv = st.session_state["cached_uv"]
            bm = calculate_burn_time(_fn, uv)
            rp = 120 if uv < 6 else 90 if uv < 9 else 60
            advice = None
            try:
                from groq import Groq
                client = Groq(api_key=st.secrets["GROQ_API_KEY"])
                p = f"Sun safety advisor for UVSense Australia. User: {_st} ({_stn}) skin, UV Index {uv}, burn time {bm} mins, reapply every {rp} mins. Write friendly 3-4 sentence personalised sun protection plan. Under 100 words. No bullet points."
                msg = client.chat.completions.create(model="llama-3.3-70b-versatile", max_tokens=250, messages=[{"role": "user", "content": p}])
                advice = msg.choices[0].message.content
            except Exception as e:
                st.error(f"API Error: {e}")
            st.session_state["ai_advice"] = advice or f"Based on your {_st} skin and current UV {uv}: you have approximately {bm} minutes before skin damage begins. Apply SPF 50+ now and reapply every {rp} minutes."
            st.session_state["ai_uv"] = uv
            st.session_state["ai_burn"] = bm
            st.session_state["ai_reapply"] = rp

        if "ai_advice" in st.session_state:
            uv = st.session_state["ai_uv"]
            bm = st.session_state["ai_burn"]
            rp = st.session_state["ai_reapply"]
            col1, col2, col3 = st.columns(3)
            col1.metric("Live UV Index", uv)
            col2.metric("Burn time", f"{bm} min")
            col3.metric("Reapply every", f"{rp} min")
            st.markdown(f"<div style='background: linear-gradient(135deg, #fff5f0 0%, #fffbea 100%); border-left: 4px solid #fb923c; border-radius: 0 12px 12px 0; padding: 1.4rem 1.6rem; margin: 1rem 0;'><p style='color: #374151; font-size: 1rem; line-height: 1.7; margin: 0;'>{st.session_state['ai_advice']}</p><p style='color: #9ca3af; font-size: 0.75rem; font-style: italic; margin: 1rem 0 0 0; padding-top: 0.8rem; border-top: 1px solid #e5e7eb;'>This is not medical advice. UVSense provides general sun safety guidance based on Cancer Council Australia and ARPANSA recommendations.</p></div>", unsafe_allow_html=True)
            st.plotly_chart(all_skin_types_chart(uv), use_container_width=True)
            st.markdown("<div style='background: #eff6ff; border-left: 4px solid #3b82f6; padding: 1rem; border-radius: 4px; margin-top: 1rem;'><strong>Data sources:</strong> Fitzpatrick (1988) skin phototype scale, WHO UV Index standard, OpenWeatherMap One Call API 3.0, Cancer Council Australia guidelines.</div>", unsafe_allow_html=True)

        st.info("Remember: All skin types can develop skin cancer. Always practice sun safety!")

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("### Understanding Fitzpatrick Skin Types")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Type I-II (Fair Skin)**\n- Always or easily burns\n- Highest risk\n- Maximum protection needed")
        st.markdown("**Type III-IV (Medium to Olive)**\n- Sometimes burns\n- Moderate risk\n- Regular protection needed")
    with col2:
        st.markdown("**Type V-VI (Dark Skin)**\n- Rarely burns\n- Lower but present risk\n- Still needs protection")
        st.markdown("**Important**\n- All skin types can get skin cancer\n- Regular skin checks recommended")