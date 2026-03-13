"""
UV Awareness Page - Educational content with charts
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd

def render():

    st.markdown("### ← Back to Dashboard", unsafe_allow_html=True)

    st.title("Understanding UV Risks in Australia")

    st.markdown("""
    <p style='font-size: 1.125rem; color: #6b7280; margin-bottom: 3rem;'>
        Learn about the impact of UV exposure and why sun protection matters for young Australians.
    </p>
    """, unsafe_allow_html=True)

    # Skin cancer data
    skin_cancer_data = pd.DataFrame({
        'Year': ['2018','2019','2020','2021','2022','2023','2024'],
        'Cases': [13200,14100,14800,15400,16200,17100,18000]
    })

    fig1 = go.Figure()

    fig1.add_trace(go.Scatter(
        x=skin_cancer_data['Year'],
        y=skin_cancer_data['Cases'],
        mode='lines+markers',
        line=dict(color='#f97316', width=3)
    ))

    st.plotly_chart(fig1, use_container_width=True)

    # Sunburn data
    uv_exposure_data = pd.DataFrame({
        'Age Group': ['18-20','21-22','23-24'],
        'Sunburn': [68,62,58],
        'Protected': [32,38,42]
    })

    fig2 = go.Figure()

    fig2.add_bar(x=uv_exposure_data['Age Group'], y=uv_exposure_data['Sunburn'], name="Sunburn")
    fig2.add_bar(x=uv_exposure_data['Age Group'], y=uv_exposure_data['Protected'], name="Protected")

    st.plotly_chart(fig2, use_container_width=True)



    