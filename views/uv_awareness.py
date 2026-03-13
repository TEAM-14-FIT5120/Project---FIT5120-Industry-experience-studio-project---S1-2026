"""
UV Awareness Page - Educational content with data visualizations
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

def render():
    st.markdown("### ← Back to Dashboard", unsafe_allow_html=True)
    
    st.title("Understanding UV Risks in Australia")
    st.markdown("""
    <p style='font-size: 1.125rem; color: #6b7280; margin-bottom: 3rem;'>
        Learn about the impact of UV exposure and why sun protection matters for young Australians.
    </p>
    """, unsafe_allow_html=True)
    
    # Skin Cancer Trends Chart
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 12])
    with col1:
        st.markdown("""
        <div style='width: 48px; height: 48px; background: linear-gradient(135deg, #f87171 0%, #f97316 100%); 
             border-radius: 50%; display: flex; align-items: center; justify-content: center;'>
            <span style='color: white; font-size: 1.5rem;'>📈</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <h2 style='margin: 0;'>Melanoma Cases in Australia (18-24 age group)</h2>
        <p style='color: #6b7280; font-size: 0.875rem; margin: 0.25rem 0 0 0;'>
            Annual diagnosed cases showing upward trend
        </p>
        """, unsafe_allow_html=True)
    
    # Create line chart data
    skin_cancer_data = pd.DataFrame({
        'Year': ['2018', '2019', '2020', '2021', '2022', '2023', '2024'],
        'Cases': [13200, 14100, 14800, 15400, 16200, 17100, 18000]
    })
    
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=skin_cancer_data['Year'],
        y=skin_cancer_data['Cases'],
        mode='lines+markers',
        name='Melanoma Cases',
        line=dict(color='#f97316', width=3),
        marker=dict(size=8, color='#f97316')
    ))
    
    fig1.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=20, b=20),
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(
            title='Year',
            showgrid=False,
            linecolor='#e5e7eb'
        ),
        yaxis=dict(
            title='Cases',
            showgrid=True,
            gridcolor='#f3f4f6',
            linecolor='#e5e7eb'
        ),
        hovermode='x unified'
    )
    
    st.plotly_chart(fig1, use_container_width=True)
    
    st.markdown("""
    <p style='text-align: center; color: #6b7280; font-size: 0.875rem; margin-top: 1rem;'>
        Melanoma diagnoses among young Australians have increased by 36% from 2018 to 2024.
    </p>
    """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)
    
    # UV Exposure Impact Chart
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 12])
    with col1:
        st.markdown("""
        <div style='width: 48px; height: 48px; background: linear-gradient(135deg, #fbbf24 0%, #f97316 100%); 
             border-radius: 50%; display: flex; align-items: center; justify-content: center;'>
            <span style='color: white; font-size: 1.5rem;'>⚠️</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <h2 style='margin: 0;'>Sunburn Rates by Age Group (2024)</h2>
        <p style='color: #6b7280; font-size: 0.875rem; margin: 0.25rem 0 0 0;'>
            Percentage of young Australians experiencing sunburn vs. protected
        </p>
        """, unsafe_allow_html=True)
    
    # Create bar chart data
    uv_exposure_data = pd.DataFrame({
        'Age Group': ['18-20', '21-22', '23-24'],
        'Experienced Sunburn (%)': [68, 62, 58],
        'Adequately Protected (%)': [32, 38, 42]
    })
    
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        x=uv_exposure_data['Age Group'],
        y=uv_exposure_data['Experienced Sunburn (%)'],
        name='Experienced Sunburn (%)',
        marker_color='#ef4444',
        marker_line_color='#ef4444',
        marker_line_width=0,
        textposition='outside'
    ))
    
    fig2.add_trace(go.Bar(
        x=uv_exposure_data['Age Group'],
        y=uv_exposure_data['Adequately Protected (%)'],
        name='Adequately Protected (%)',
        marker_color='#22c55e',
        marker_line_color='#22c55e',
        marker_line_width=0,
        textposition='outside'
    ))
    
    fig2.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=20, b=20),
        plot_bgcolor='white',
        paper_bgcolor='white',
        barmode='group',
        xaxis=dict(
            title='Age Group',
            showgrid=False,
            linecolor='#e5e7eb'
        ),
        yaxis=dict(
            title='Percentage (%)',
            showgrid=True,
            gridcolor='#f3f4f6',
            linecolor='#e5e7eb',
            range=[0, 80]
        ),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1
        ),
        hovermode='x unified'
    )
    
    st.plotly_chart(fig2, use_container_width=True)
    
    st.markdown("""
    <p style='text-align: center; color: #6b7280; font-size: 0.875rem; margin-top: 1rem;'>
        Over 60% of young Australians report experiencing sunburn in the past year, indicating inadequate sun protection.
    </p>
    """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div style='margin: 3rem 0;'></div>", unsafe_allow_html=True)
    
    # Educational Info Cards
    st.markdown("<h2 style='margin-bottom: 1.5rem;'>Key Facts About UV Protection</h2>", 
                unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class='card'>
            <div style='width: 64px; height: 64px; background: linear-gradient(135deg, #f87171 0%, #f97316 100%); 
                 border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; 
                 margin-bottom: 1rem;'>
                <span style='color: white; font-size: 2rem;'>⚠️</span>
            </div>
            <h3 style='margin-bottom: 1rem;'>Why UV Matters</h3>
            <p style='color: #6b7280; line-height: 1.6;'>
                Australia has one of the highest rates of skin cancer in the world. 
                UV radiation damages skin cells and can lead to melanoma.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='card'>
            <div style='width: 64px; height: 64px; background: linear-gradient(135deg, #fb923c 0%, #fbbf24 100%); 
                 border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; 
                 margin-bottom: 1rem;'>
                <span style='color: white; font-size: 2rem;'>📈</span>
            </div>
            <h3 style='margin-bottom: 1rem;'>Rising Risk for Youth</h3>
            <p style='color: #6b7280; line-height: 1.6;'>
                Young Australians aged 18-24 show increasing rates of sunburn incidents, 
                especially during summer outdoor activities.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='card'>
            <div style='width: 64px; height: 64px; background: linear-gradient(135deg, #3b82f6 0%, #a855f7 100%); 
                 border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; 
                 margin-bottom: 1rem;'>
                <span style='color: white; font-size: 2rem;'>⚠️</span>
            </div>
            <h3 style='margin-bottom: 1rem;'>Prevention is Key</h3>
            <p style='color: #6b7280; line-height: 1.6;'>
                Most skin cancers are preventable with proper sun protection. 
                Regular sunscreen use can reduce melanoma risk by 50%.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div style='margin: 3rem 0;'></div>", unsafe_allow_html=True)
    
    # Call to Action
    st.markdown("""
    <div style='background: linear-gradient(135deg, #f97316 0%, #fbbf24 100%); 
         padding: 2rem; border-radius: 12px; text-align: center; color: white; 
         box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);'>
        <h3 style='margin-bottom: 1rem;'>Take Action Today</h3>
        <p style='opacity: 0.9; max-width: 600px; margin: 0 auto 1.5rem auto;'>
            Understanding UV risks is the first step. Use our tools to find personalized 
            protection advice and start protecting your skin now.
        </p>
    </div>
    """, unsafe_allow_html=True)
