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

st.title("Cancer Trends by Age Group")

if not df.empty:
    # 2. Extract unique age groups (e.g., '0-4', '5-9')
    # We sort them so they appear in chronological order
    age_options = sorted(df['Age group (years)'].unique())

    # 3. Create clickable age selection
    selected_age = st.pills(
        "Select Age Group Band:",
        options=age_options,
        default=age_options[0]
    )

    if selected_age:
        # 4. Filter the data for the selected 5-year band
        # This keeps only the rows matching '0-4', etc.
        filtered_df = df[df['Age group (years)'] == selected_age]

        # 5. Aggregate by Year and Cancer Type
        # We sum the 'Count' to get a single data point per year/type
        trend_data = filtered_df.groupby('Year')['Count'].sum().reset_index()

        st.subheader(f"Yearly Trend for Age Group {selected_age}")
        
        # 6. Display the trend chart
        st.line_chart(
            trend_data, 
            x="Year", 
            y="Count", 
        )