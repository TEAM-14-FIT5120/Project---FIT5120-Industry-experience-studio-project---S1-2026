"""
Skin Type Tool - Personalized protection recommendations  
With AI Sun Protection Advisor powered by Claude API
"""
import streamlit as st
from views.get_live_uv import get_weather_data

def get_ai_protection_advice(skin_type_label, risk_level, uv_index, burn_minutes):
    try:
        import anthropic
        reapply = 120 if uv_index < 6 else 90 if uv_index < 9 else 60
        prompt = f"""You are a friendly sun safety advisor for UVSense, an Australian sun protection app built by Monash University students. Grounded in Cancer Council Australia and ARPANSA guidelines.
User: Fitzpatrick {skin_type_label}, Risk: {risk_level}, UV Index: {uv_index}, Burn time: {burn_minutes} mins, Reapply every: {reapply} mins.
Australia has the world highest melanoma rate - 2 in 3 Australians develop skin cancer.
Write a friendly 3-4 sentence protection plan. Be specific with numbers. Speak as you. Under 100 words. No bullet points."""
        client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
        message = client.messages.create(model="claude-sonnet-4-6", max_tokens=250, messages=[{"role": "user", "content": prompt}])
        return message.content[0].text
    except:
        return None

def calculate_burn_time(fitzpatrick_num, uv_index):
    base_times = {1: 67, 2: 100, 3: 133, 4: 200, 5: 300, 6: 400}
    if uv_index <= 0:
        return 999
    return max(1, round(base_times.get(fitzpatrick_num, 133) / uv_index))

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
            st.session_state.skin_type, st.session_state.skin_type_name, st.session_state.risk_level, st.session_state.risk_color, st.session_state.fitzpatrick_num = "Type I", "Very Fair", "Extreme Risk", "#dc2626", 1
            st.session_state.recommendations = ["Apply SPF 50+ sunscreen every 90 minutes", "Always wear a wide-brimmed hat outdoors", "Wear long sleeves and pants when possible", "UV-blocking sunglasses are essential", "Seek shade between 10am-4pm", "Limit sun exposure to less than 30 minutes", "Avoid tanning beds completely"]
        elif score <= 5:
            st.session_state.skin_type, st.session_state.skin_type_name, st.session_state.risk_level, st.session_state.risk_color, st.session_state.fitzpatrick_num = "Type II", "Fair", "High Risk", "#ea580c", 2
            st.session_state.recommendations = ["Apply SPF 30-50 sunscreen every 2 hours", "Wear a hat when outdoors for extended periods", "Cover up during peak sun hours", "Wear UV-protective sunglasses", "Seek shade during midday hours", "Build up sun exposure gradually", "Use UV index apps to plan activities"]
        elif score <= 9:
            st.session_state.skin_type, st.session_state.skin_type_name, st.session_state.risk_level, st.session_state.risk_color, st.session_state.fitzpatrick_num = "Type III", "Medium", "Moderate Risk", "#f59e0b", 3
            st.session_state.recommendations = ["Apply SPF 30+ sunscreen every 2-3 hours", "Wear a hat during extended outdoor activities", "Use UV-protective sunglasses", "Take shade breaks during peak hours", "Reapply sunscreen after swimming", "Be extra cautious at beach or pool", "Monitor UV index daily"]
        elif score <= 13:
            st.session_state.skin_type, st.session_state.skin_type_name, st.session_state.risk_level, st.session_state.risk_color, st.session_state.fitzpatrick_num = "Type IV", "Olive", "Moderate Risk", "#f59e0b", 4
            st.session_state.recommendations = ["Apply SPF 30 sunscreen every 3 hours", "Wear sunglasses for eye protection", "Hat recommended for extended exposure", "Seek shade when UV index is high", "Reapply after swimming or sweating", "Extra protection at beach/snow", "Still vulnerable to UV damage"]
        else:
            st.session_state.skin_type, st.session_state.skin_type_name, st.session_state.risk_level, st.session_state.risk_color, st.session_state.fitzpatrick_num = "Type V-VI", "Dark", "Lower Risk", "#10b981", 5
            st.session_state.recommendations = ["Apply SPF 15-30 sunscreen daily", "Wear sunglasses for eye protection", "Reapply sunscreen every 3-4 hours", "Extra protection during water activities", "Shade recommended during peak UV", "Still need sun protection", "Check UV index for outdoor planning"]
        st.session_state.quiz_done = True

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
            with st.spinner("Fetching live UV data..."):
                weather_data = get_weather_data()
                uv_index = round(weather_data.get("current", {}).get("uvi", 6)) if weather_data else 6
            burn_minutes = calculate_burn_time(st.session_state.fitzpatrick_num, uv_index)
            reapply = 120 if uv_index < 6 else 90 if uv_index < 9 else 60
            col1, col2, col3 = st.columns(3)
            col1.metric("Live UV Index", uv_index)
            col2.metric("Burn time", f"{burn_minutes} min")
            col3.metric("Reapply every", f"{reapply} min")
            with st.spinner("Generating your personalised plan..."):
                advice = get_ai_protection_advice(f"{st.session_state.skin_type} ({st.session_state.skin_type_name})", st.session_state.risk_level, uv_index, burn_minutes)
            if advice:
                st.session_state.ai_advice = advice
                st.session_state.ai_uv = uv_index
                st.session_state.ai_burn = burn_minutes
                st.session_state.ai_reapply = reapply
            else:
                st.session_state.ai_advice = f"Based on your {st.session_state.skin_type} skin and current UV {uv_index}: you have approximately {burn_minutes} minutes before skin damage begins. Apply SPF 50+ now and reapply every {reapply} minutes."
                st.session_state.ai_uv = uv_index
                st.session_state.ai_burn = burn_minutes
                st.session_state.ai_reapply = reapply

        if st.session_state.get("ai_advice"):
            col1, col2, col3 = st.columns(3)
            col1.metric("Live UV Index", st.session_state.ai_uv)
            col2.metric("Burn time", f"{st.session_state.ai_burn} min")
            col3.metric("Reapply every", f"{st.session_state.ai_reapply} min")
            st.markdown(f"<div style='background: linear-gradient(135deg, #fff5f0 0%, #fffbea 100%); border-left: 4px solid #fb923c; border-radius: 0 12px 12px 0; padding: 1.4rem 1.6rem; margin: 1rem 0;'><p style='color: #374151; font-size: 1rem; line-height: 1.7; margin: 0;'>{st.session_state.ai_advice}</p><p style='color: #9ca3af; font-size: 0.75rem; font-style: italic; margin: 1rem 0 0 0; padding-top: 0.8rem; border-top: 1px solid #e5e7eb;'>This is not medical advice. UVSense provides general sun safety guidance based on Cancer Council Australia and ARPANSA recommendations.</p></div>", unsafe_allow_html=True)

        st.info("Remember: All skin types can develop skin cancer. Always practice sun safety!")

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("### Understanding Fitzpatrick Skin Types")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Type I-II (Fair Skin)**\n- Always or easily burns\n- Never or rarely tans\n- Highest risk\n- Maximum protection needed")
        st.markdown("**Type III-IV (Medium to Olive)**\n- Sometimes burns\n- Tans gradually\n- Moderate risk\n- Regular protection needed")
    with col2:
        st.markdown("**Type V-VI (Dark Skin)**\n- Rarely burns\n- Tans easily\n- Lower but present risk\n- Still needs protection")
        st.markdown("**Important**\n- All skin types can get skin cancer\n- Regular skin checks recommended")
