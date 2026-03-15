"""
UV Awareness Page - Educational content with data visualizations
"""

from matplotlib import scale
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import pandas as pd
conn = st.connection("neon", type="sql")

query = "SELECT * FROM cancer_stats;"
df = conn.query(query, ttl="10m")
query2 = 'SELECT * FROM sunburn_stats;'
chart_2_df = conn.query(query2, ttl="10m")

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
    
    df['Year'] = pd.to_numeric(df['Year'])
    df['Count'] = pd.to_numeric(df['Count'])

# 2. Group by Year and sum the Counts
    yearly_counts = df.groupby('Year')['Count'].sum().reset_index()

# 3. Rename columns for a cleaner chart (optional)
    yearly_counts.columns = ['Year', 'Total Cases']
    
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=yearly_counts['Year'],
        y=yearly_counts['Total Cases'],
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

    val_2008 = df[df['Year'] == 2008]['Count'].sum()
    val_2022 = df[df['Year'] == 2022]['Count'].sum()

# 5. Calculate percentage increase
    if val_2008 > 0:
        percentage_change = ((val_2022 - val_2008) / val_2008) * 100
        display_percent = round(abs(percentage_change))
        direction = "increased" if percentage_change > 0 else "decreased"
    else:
        display_percent = 0
        direction = "changed"
        
    st.markdown(f"""
    <p style='text-align: center; color: #6b7280; font-size: 0.875rem; margin-top: 1rem;'>
        Melanoma diagnoses among young Australians have {direction} by {display_percent}% from 2008 to 2022.
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
            Percentage of young Australians experiencing sunburn
        </p>
        """, unsafe_allow_html=True)
    
    # Create waffle chart data
    
    pop_col = 'Population at 30 June 2024 (\'000)'
    tan_col = 'Proportion (%)_tan'

    # Calculate the actual population impact (Volume)
    chart_2_df['Impact_Score'] = chart_2_df[pop_col] * chart_2_df[tan_col]
    max_impact = chart_2_df['Impact_Score'].max()
    
    def render_tanning_row(region, pct, scale):
        # 1. The SVG Icon Template
        svg_template = """
        <svg width="22" height="45" viewBox="0 0 20 40" style="margin-right: 2px;">
            <defs>
                <linearGradient id="grad_{id}" x1="0%" y1="100%" x2="0%" y2="0%">
                    <stop offset="{fill}%" style="stop-color:#fbbf24;stop-opacity:1" />
                    <stop offset="{fill}%" style="stop-color:#e5e7eb;stop-opacity:1" />
                </linearGradient>
            </defs>
            <path d="M10 2c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3zm5 7h-1c-.55 0-1 .45-1 1v7h-1v19c0 .55-.45 1-1 1h-4c-.55 0-1-.45-1-1v-19h-1v-7c0-.55-.45-1-1-1h-1c-.55 0-1 .45-1 1v8c0 .55.45 1 1 1h1v19c0 1.1.9 2 2 2h4c1.1 0 2-.9 2-2v-19h1c.55 0 1-.45 1-1v-8c0-.55-.45-1-1-1z" 
                fill="url(#grad_{id})" />
        </svg>
        """
        
        icons_html = ""
        for i in range(10):
            lower_bound = i * 10
            fill = max(0, min(100, (pct - lower_bound) * 10))
            icons_html += svg_template.format(id=f"{region.replace(' ', '_')}_{i}", fill=fill)

        row_width = int(max(160, 480 * scale))

        html_row = (f"""
        <div style="display: flex; align-items: center; margin-bottom: 12px; padding: 10px; border-bottom: 1px solid #f1f5f9;">
            <div style="width: 140px; font-weight: 600; font-size: 0.9rem; color: #334155;">{region}</div>
            <div style="display: flex; width: {row_width}px; justify-content: start;">
                {icons_html}
            </div>
            <div style="margin-left: 20px; font-size: 0.85rem; color: #64748b;">
                <b style="color: #d97706; font-size: 1.1rem;">{pct}%</b><br>intent to tan
            </div>
        </div>
        """)
        
        return html_row.format(reg=region, width=row_width, icons=icons_html, val=pct)
        
    st.markdown("""
        Each row represents a state. Shaded icons show the percentage of people 
        actively seeking a suntan. **Wider rows** indicate a higher total population impact.
    """, unsafe_allow_html=True)
    
    
    sorted_df = chart_2_df.sort_values(by='Impact_Score', ascending=False)

    for _, row in sorted_df.iterrows():
        current_scale = row['Impact_Score'] / max_impact
        st.markdown(
            render_tanning_row(row['Region'], row[tan_col], current_scale), 
            unsafe_allow_html=True
        )
    
    
    
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
