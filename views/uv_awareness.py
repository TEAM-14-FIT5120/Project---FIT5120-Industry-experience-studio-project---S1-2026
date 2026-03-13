"""
UV Awareness Page - Educational content with data visualizations
"""

import streamlit as st

def render():

    st.markdown("### ← Back to Dashboard", unsafe_allow_html=True)

    st.title("Understanding UV Risks in Australia")

    st.markdown("""
    <p style='font-size: 1.125rem; color: #6b7280; margin-bottom: 3rem;'>
        Learn about the impact of UV exposure and why sun protection matters for young Australians.
    </p>
    """, unsafe_allow_html=True)