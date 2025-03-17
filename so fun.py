import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from datetime import datetime
import numpy as np
# Set page configuration
st.set_page_config(page_title="Player Performance Dashboard", layout="wide")
# File upload section
st.sidebar.header("Data Upload")
uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type=['csv']) 
if uploaded_file is not None:
        try:
# Read the CSV file
                df = pd.read_csv(uploaded_file)
# Convert session_date to datetime
                df['sessionDate'] = pd.to_datetime(df['sessionDate'])
# Sidebar filters
                st.sidebar.header("Filters")
# Season filter
                seasons = ['All'] + sorted(df['seasonName'].unique().tolist())
                selected_season = st.sidebar.selectbox("Select Season", seasons)
# Category filter
                categories = ['All'] + sorted(df['category'].unique().tolist())
                selected_category = st.sidebar.selectbox("Select Category", categories)
# Metric filter
                metrics = ['All'] + sorted(df['metric'].unique().tolist())
                selected_metrics = st.sidebar.multiselect("Select Metrics", metrics, default='All')
        
        # Date range filter
                date_range = st.sidebar.date_input(
                    "Select Date Range",
                    [df['sessionDate'].min(), df['sessionDate'].max()]
        )
        
        # Filter data based on selections
        finally : filtered_df = df.copy()
        
        if selected_season != 'All':
            filtered_df = filtered_df[filtered_df['seasonName'] == selected_season]
        
        if selected_category != 'All':
            filtered_df = filtered_df[filtered_df['category'] == selected_category]
            
        if 'All' not in selected_metrics:
            filtered_df = filtered_df[filtered_df['metric'].isin(selected_metrics)]
            
        filtered_df = filtered_df[
            (filtered_df['sessionDate'].dt.date >= date_range[0]) & 
            (filtered_df['sessionDate'].dt.date <= date_range[1])
        ]
        
        # Dashboard title
        st.title("Player Performance Analytics Dashboard")
        
        # Main dashboard layout
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Metric Trends Over Time")
            # Create line plot for selected metrics
            fig_trends = px.line(
                filtered_df,
                x='sessionDate',
                y='value',
                color='metric',
                title="Metric Trends Over Time"
            )
            fig_trends.update_layout(height=400)
            st.plotly_chart(fig_trends, use_container_width=True)
            
        with col2:
            st.subheader("Category Distribution")
            # Box plot for value distribution by category
            fig_box = px.box(
                filtered_df,
                x='category',
                y='value',
                color='metric',
                title="Value Distribution by Category"
            )
            fig_box.update_layout(height=400)
            st.plotly_chart(fig_box, use_container_width=True)
        
        # Seasonal comparison
        st.subheader("Seasonal Comparison")
        col3, col4 = st.columns(2)
        
        with col3:
            # Calculate seasonal averages
            seasonal_avg = df.groupby(['seasonName', 'metric'])['value'].mean().reset_index()
            fig_seasonal = px.bar(
                seasonal_avg,
                x='seasonName',
                y='value',
                color='metric',
                title="Average Values by Season",
                barmode='group'
            )
            st.plotly_chart(fig_seasonal, use_container_width=True)
            
        with col4:
            # Recent trends table
            st.subheader("Recent Values")
            recent_values = filtered_df.sort_values('sessionDate', ascending=False)
            recent_pivot = recent_values.pivot_table(
                index='sessionDate',
                columns='metric',
                values='value',
                aggfunc='first'
            ).round(2).head(5)
            st.write(recent_pivot)
        
        # Statistical Summary
        st.subheader("Statistical Summary")
        col5, col6 = st.columns(2)
        
        with col5:
            # Summary statistics
            summary_stats = filtered_df.groupby('metric')['value'].agg([
                'count', 'mean', 'std', 'min', 'max'
            ]).round(2)
            st.write(summary_stats)
            
        with col6:
            # Correlation heatmap between metrics
            pivot_data = filtered_df.pivot_table(
                index='sessionDate',
                columns='metric',
                values='value'
            )
            correlation = pivot_data.corr()
            fig_corr = px.imshow(
                correlation,
                title="Metric Correlations",
                color_continuous_scale="RdBu"
            )
            st.plotly_chart(fig_corr, use_container_width=True)
        
        # Download filtered data
        st.download_button(
            label="Download filtered data as CSV",
            data=filtered_df.to_csv(index=False).encode('utf-8'),
            file_name='filtered_performance_data.csv',
            mime='text/csv',
        )
        
        # Data quality indicators
        st.subheader("Data Quality Indicators")
        missing_values = filtered_df.isnull().sum()
        if missing_values.sum() > 0:
            st.warning("Missing values detected in the dataset")
            st.write(missing_values[missing_values > 0])
try:
    # Your main code block should be here
    values='value'
    correlation = pivot_data.corr()
    fig_corr = px.imshow(
        correlation,
        title="Metric Correlations",
        color_continuous_scale="RdBu"
    )
    st.plotly_chart(fig_corr, use_container_width=True)

    # Download filtered data
    st.download_button(
        label="Download filtered data as CSV",
        data=filtered_df.to_csv(index=False).encode('utf-8'),
        file_name='filtered_performance_data.csv',
        mime='text/csv',
    )

    # Data quality indicators
    st.subheader("Data Quality Indicators")
    missing_values = filtered_df.isnull().sum()
    if missing_values.sum() > 0:
        st.warning("Missing values detected in the dataset")
        st.write(missing_values[missing_values > 0])

except Exception as e:
    st.error(f"Error processing the file: {str(e)}")
    st.write("Please ensure your CSV file has the correct format with columns: session_date, season_name, metric, category, and value")
else:
    # This will execute if no exception occurs
    st.write("Please upload a CSV file to begin analysis")
    
    # Display expected CSV format
    st.subheader("Expected CSV Format:")
    st.write("""
    Your CSV file should have the following columns:
    - session_date: Date of the session
    - season_name: Name or ID of the season
    - metric: Name of the performance metric
    - category: Category of the metric
    - value: Numerical value of the metric
    
    Example:
    | sessionDate | seasonName | metric        | category | value |
    |--------------|-------------|---------------|----------|-------|
    | 2023-01-01  | 2022/23     | Sleep_Hours   | Recovery | 7.5   |
    | 2023-01-01  | 2022/23     | Muscle_Sore   | Wellness | 3.0   |
    """)
