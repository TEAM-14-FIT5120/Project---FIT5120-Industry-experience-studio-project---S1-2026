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