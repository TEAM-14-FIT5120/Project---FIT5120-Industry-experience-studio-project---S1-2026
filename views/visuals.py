""" The visualisations tab from the database in neon"""

import streamlit as st
import pandas as pd
conn = st.connection("neon", type="sql")

# 2. Query Data (With 10-minute cache to save Neon compute)
query = "SELECT * FROM cancer_stats;"
df = conn.query(query, ttl="10m")

# 3. Simple Visuals
st.subheader("Raw Data Preview")
st.dataframe(df.head())

st.subheader("Chart 1: Cumulative Cancer Counts by Year")

    # 1. Group the data by 'report_year' and sum the 'incident_count'
    # This combines all age groups and cancer types into one total per year
df_cumulative = df.groupby(['Year', 'Cancer group/site'])['Count'].sum().reset_index()

    # 2. Display the Cumulative Chart
    # We use the new 'df_cumulative' dataframe here
st.line_chart(
    df_cumulative, 
    x="Year", 
    y="Count", 
    color="Cancer group/site"
)
    
st.caption("This chart shows the total combined incident count for all age groups and cancer types per year.")
    

