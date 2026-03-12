import streamlit as st


def render():
    # Top spacing
    st.markdown("<div style='margin-top: 0.5rem;'></div>", unsafe_allow_html=True)

    # Location
    st.markdown("""
    <div style='text-align: center; margin: 1rem 0 1.5rem 0;'>
        <p style='color: #6b7280; display: flex; align-items: center; justify-content: center; gap: 0.5rem; font-size: 1rem; margin: 0;'>
            <span style='width: 10px; height: 10px; background: #22c55e; border-radius: 50%; display: inline-block;'></span>
            Melbourne, Australia
        </p>
    </div>
    """, unsafe_allow_html=True)

    # UV gauge centered
    center_col = st.columns([1, 2, 1])[1]
    with center_col:
        st.markdown("""
        <div style='display: flex; justify-content: center; margin-bottom: 1.5rem;'>
            <div class='uv-gauge'>
                <div style='font-size: 2.5rem; line-height: 1;'>☀️</div>
                <p class='uv-number'>8</p>
                <p class='uv-label'>UV Index</p>
                <p class='uv-level'>High</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Warning banner
    st.markdown("""
    <div class='warning-banner'>
        ⚠️ High UV – skin damage may occur quickly. Minimise sun exposure from 10 AM to 4 PM.
    </div>
    """, unsafe_allow_html=True)


    st.markdown("<div style='margin: 2rem 0 1rem 0;'></div>", unsafe_allow_html=True)

    # Section title
    st.markdown("""
    <h1 style='text-align: center; color: #1f2937; font-size: 2.5rem; margin-bottom: 2rem;'>
        Protection Advice
    </h1>
    """, unsafe_allow_html=True)

    # First row
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("""
        <div class='protection-card'>
            <div style='width: 56px; height: 56px; border-radius: 50%; background: linear-gradient(135deg, #60a5fa 0%, #2563eb 100%);
                        display: flex; align-items: center; justify-content: center; margin: 0 auto 1rem auto; font-size: 1.6rem; color: white;'>
                💧
            </div>
            <h3 style='margin-bottom: 0.5rem; color: #1f2937; font-size: 1.8rem;'>Apply Sunscreen</h3>
            <p style='color: #6b7280; font-size: 1rem; margin: 0;'>SPF 30+ every 2 hours</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='protection-card'>
            <div style='width: 56px; height: 56px; border-radius: 50%; background: linear-gradient(135deg, #c084fc 0%, #9333ea 100%);
                        display: flex; align-items: center; justify-content: center; margin: 0 auto 1rem auto; font-size: 1.6rem; color: white;'>
                🕶️
            </div>
            <h3 style='margin-bottom: 0.5rem; color: #1f2937; font-size: 1.8rem;'>Wear Sunglasses</h3>
            <p style='color: #6b7280; font-size: 1rem; margin: 0;'>UV protective lenses</p>
        </div>
        """, unsafe_allow_html=True)



    