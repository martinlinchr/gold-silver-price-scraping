import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
from price_scraper import load_data

st.title('Gold and Silver Price Tracker')

# Load and preprocess the data
df = load_data()
if not df.empty:
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df = df.sort_values('Timestamp')

    # Display the most recent prices
    latest_data = df.iloc[-1]
    st.subheader('Latest Prices')
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Gold Price (1000g)", f"€{latest_data['Gold Price']:.2f}")
        st.metric("Gold Price (100g)", f"€{latest_data['Gold Price']/10:.2f}")
        st.metric("Gold Price (1g)", f"€{latest_data['Gold Price']/1000:.2f}")
    with col2:
        st.metric("Silver Price (1000g)", f"€{latest_data['Silver Price']:.2f}")
        st.metric("Silver Price (100g)", f"€{latest_data['Silver Price']/10:.2f}")
        st.metric("Silver Price (1g)", f"€{latest_data['Silver Price']/1000:.2f}")
    with col3:
        st.metric("Gold-Silver Ratio", f"{latest_data['Gold-Silver Ratio']:.2f}")
    
    st.text(f"Last updated: {latest_data['Timestamp']}")

    # Date range selection
    st.subheader('Select Date Range')
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start date", df['Timestamp'].min().date())
    with col2:
        end_date = st.date_input("End date", df['Timestamp'].max().date())
    
    mask = (df['Timestamp'].dt.date >= start_date) & (df['Timestamp'].dt.date <= end_date)
    df_filtered = df.loc[mask]
    
    if df_filtered.empty:
        st.warning("No data available for the selected date range.")
    else:
        # Display statistics
        st.subheader('Price Statistics')
        stats = pd.DataFrame({
            'Metric': ['Lowest', 'Highest', 'Average'],
            'Gold Price (1000g)': [
                f"€{df_filtered['Gold Price'].min():.2f}",
                f"€{df_filtered['Gold Price'].max():.2f}",
                f"€{df_filtered['Gold Price'].mean():.2f}"
            ],
            'Gold Price (100g)': [
                f"€{df_filtered['Gold Price'].min() / 10:.2f}",
                f"€{df_filtered['Gold Price'].max() / 10:.2f}",
                f"€{df_filtered['Gold Price'].mean() / 10:.2f}"
            ],
            'Gold Price (1g)': [
                f"€{df_filtered['Gold Price'].min() / 1000:.2f}",
                f"€{df_filtered['Gold Price'].max() / 1000:.2f}",
                f"€{df_filtered['Gold Price'].mean() / 1000:.2f}"
            ],
            'Silver Price (1000g)': [
                f"€{df_filtered['Silver Price'].min():.2f}",
                f"€{df_filtered['Silver Price'].max():.2f}",
                f"€{df_filtered['Silver Price'].mean():.2f}"
            ],
            'Silver Price (100g)': [
                f"€{df_filtered['Silver Price'].min() / 10:.2f}",
                f"€{df_filtered['Silver Price'].max() / 10:.2f}",
                f"€{df_filtered['Silver Price'].mean() / 10:.2f}"
            ],
            'Silver Price (1g)': [
                f"€{df_filtered['Silver Price'].min() / 1000:.2f}",
                f"€{df_filtered['Silver Price'].max() / 1000:.2f}",
                f"€{df_filtered['Silver Price'].mean() / 1000:.2f}"
            ],
            'Gold-Silver Ratio': [
                f"{df_filtered['Gold-Silver Ratio'].min():.2f}",
                f"{df_filtered['Gold-Silver Ratio'].max():.2f}",
                f"{df_filtered['Gold-Silver Ratio'].mean():.2f}"
            ]
        })
        st.table(stats)
        
        # Create line charts
        st.subheader('Price and Ratio Charts')
        fig_gold = px.line(df_filtered, x='Timestamp', y='Gold Price', title='Gold Price Over Time (1000g)')
        st.plotly_chart(fig_gold)
        fig_silver = px.line(df_filtered, x='Timestamp', y='Silver Price', title='Silver Price Over Time (1000g)')
        st.plotly_chart(fig_silver)
        fig_ratio = px.line(df_filtered, x='Timestamp', y='Gold-Silver Ratio', title='Gold-Silver Ratio Over Time')
        st.plotly_chart(fig_ratio)
        
        # Display raw data
        st.subheader('Raw Data')
        st.dataframe(df_filtered)
else:
    st.info("No data available. Please wait for the next scheduled update.")

# Add some instructions
st.sidebar.header("Instructions")
st.sidebar.info(
    "This app displays the gold and silver prices, and the gold-silver ratio from thesilvermountain.nl. "
    "The data is updated daily at 5:00 AM UTC via GitHub Actions. "
    "Use the date range selector to view statistics and charts for specific time periods. "
    "The app displays the latest prices, price statistics, charts, and raw data for the selected date range."
)
