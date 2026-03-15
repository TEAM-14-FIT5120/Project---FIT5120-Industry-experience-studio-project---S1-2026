"""
UV Awareness Page - Educational content with data visualizations
"""

from matplotlib import scale as mpl_scale
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import streamlit.components.v1 as components
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
    burn_col = 'Proportion (%)_sunburn'
    MIN_ICONS = 5
    MAX_ICONS = 15
    count_col = 'count_sunburn'
    chart_2_df['count_sunburnt'] = chart_2_df[pop_col] * (chart_2_df[burn_col]*1000)
    
    max_c = chart_2_df[count_col].max()
    min_c = chart_2_df[count_col].min()

    # Calculate the actual population impact (Volume)
    chart_2_df['Impact_Score'] = chart_2_df[pop_col] * chart_2_df[burn_col]
    max_impact = chart_2_df['Impact_Score'].max()
    
    def render_risk_row(region, sunburn_pct, n_icons,percentage_sunburn):
    # Template for one icon: Yellow background (Tanners), Red fill (Sunburns)
        svg_icon = """
        <svg width="20" height="20" viewBox="0 0 20 20" style="margin-right:4px; display:inline-block;">
            <defs>
                <linearGradient id="grad_[[ID]]_[[I]]" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop offset="[[FILL]]%" style="stop-color:#ef4444; stop-opacity:1"/>
                    <stop offset="[[FILL]]%" style="stop-color:#fbbf24; stop-opacity:1"/>
                </linearGradient>
            </defs>
            <circle cx="10" cy="10" r="8" fill="url(#grad_[[ID]]_[[I]])" />
        </svg>
        """
        
        icons_html = ""
        clean_id = "".join(filter(str.isalnum, region))
        
        for i in range(n_icons):
            # Determine the percentage range for this specific circle
            lower_bound = i * (100 / n_icons)
            upper_bound = (i + 1) * (100 / n_icons)
            
            if sunburn_pct >= upper_bound:
                fill_pct = 100  # 100% Red
            elif sunburn_pct <= lower_bound:
                fill_pct = 0    # 100% Yellow
            else:
                # For the middle circle, calculate exactly where the sharp cut should be
                fill_pct = (sunburn_pct - lower_bound) / (upper_bound - lower_bound) * 100
        
        # We use two layered divs. The red one is clipped to show the yellow underneath.
            icons_html += f"""
            <div style="position: relative; width: 18px; height: 18px; margin-right: 4px; flex-shrink: 0; display: inline-block;">
                <div style="position: absolute; width: 100%; height: 100%; background-color: #fbbf24; border-radius: 50%;"></div>
                
                <div style="position: absolute; width: 100%; height: 100%; background-color: #ef4444; border-radius: 50%; 
                            clip-path: inset(0 {100 - fill_pct}% 0 0);"></div>
            </div>
            """
        
        layout = f"""
        <div style="display: flex; align-items: center; margin-bottom: 8px; padding: 10px; border-bottom: 1px solid #f1f5f9; font-family: sans-serif; background-color: white;">
            <div style="width: 150px; font-weight: 600; font-size: 14px; color: #334155; flex-shrink: 0;">{region}</div>
            <div style="display: flex; flex-direction: row; flex-wrap: nowrap; align-items: center; flex-grow: 1;">
                {icons_html}
            </div>
            <div style="margin-left: 20px; text-align: right; width: 100px; flex-shrink: 0;">
                <span style="color: #ef4444; font-weight: 700; font-size: 16px;">{percentage_sunburn}%</span>
                <div style="font-size: 11px; color: #94a3b8;"> of total population</div>
            </div>
        </div>
        """
        return layout
    
    
    all_rows_html = '<div style="background-color: white; padding: 10px; border-radius: 10px;">'

# Sort so most tanners are at the top
    sorted_df = chart_2_df.sort_values(by=count_col, ascending=False)
    max_impact = sorted_df[count_col].max()
    min_impact = sorted_df[count_col].min()

    for _, row in sorted_df.iterrows():
        # Linear scale for 5 to 15 icons
        scale = (row['Impact_Score'] - min_impact) / (max_impact - min_impact) if max_impact != min_impact else 0.5
        n_icons = int(5 + (10 * scale))
        
        all_rows_html += render_risk_row(row['Region'], (row['count_sunburnt']/row[count_col]), n_icons,row['Proportion (%)_sunburn'])
    all_rows_html += '</div>'

# 3. Display the component
    components.html(all_rows_html, height=600, scrolling=True)
    
    
    
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
