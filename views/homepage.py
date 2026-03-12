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

    st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)

    # Second row
    col3, col4 = st.columns(2, gap="large")

    with col3:
        st.markdown("""
        <div class='protection-card'>
            <div style='width: 56px; height: 56px; border-radius: 50%; background: linear-gradient(135deg, #fb923c 0%, #f97316 100%);
                        display: flex; align-items: center; justify-content: center; margin: 0 auto 1rem auto; font-size: 1.6rem; color: white;'>
                👒
            </div>
            <h3 style='margin-bottom: 0.5rem; color: #1f2937; font-size: 1.8rem;'>Wear a Hat</h3>
            <p style='color: #6b7280; font-size: 1rem; margin: 0;'>Wide-brimmed hat preferred</p>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class='protection-card'>
            <div style='width: 56px; height: 56px; border-radius: 50%; background: linear-gradient(135deg, #34d399 0%, #059669 100%);
                        display: flex; align-items: center; justify-content: center; margin: 0 auto 1rem auto; font-size: 1.6rem; color: white;'>
                🌳
            </div>
            <h3 style='margin-bottom: 0.5rem; color: #1f2937; font-size: 1.8rem;'>Seek Shade</h3>
            <p style='color: #6b7280; font-size: 1rem; margin: 0;'>Stay indoors during peak UV hours</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin: 2.5rem 0 1rem 0;'></div>", unsafe_allow_html=True)

    # Extra info cards
    info1, info2 = st.columns(2, gap="large")

    with info1:
        st.markdown("""
        <div class='card'>
            <h3 style='margin-top: 0; color: #1f2937;'>Today's UV Summary</h3>
            <p style='color: #6b7280; margin-bottom: 0.5rem;'>
                UV levels are high today in Melbourne. Outdoor protection is strongly recommended.
            </p>
            <ul style='color: #6b7280; padding-left: 1.2rem; margin-bottom: 0;'>
                <li>Peak UV hours: 10:00 AM – 4:00 PM</li>
                <li>Recommended SPF: 30+</li>
                <li>Reapply sunscreen every 2 hours</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with info2:
        st.markdown("""
        <div class='card'>
            <h3 style='margin-top: 0; color: #1f2937;'>Quick Tips</h3>
            <p style='color: #6b7280; margin-bottom: 0.5rem;'>
                Simple actions can reduce UV exposure significantly.
            </p>
            <ul style='color: #6b7280; padding-left: 1.2rem; margin-bottom: 0;'>
                <li>Check UV before leaving home</li>
                <li>Carry sunscreen in your bag</li>
                <li>Choose shaded outdoor areas</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)