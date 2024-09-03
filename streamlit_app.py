import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
from price_scraper import scrape_price, scrape_ratio, load_data, save_data

st.title('Gold and Silver Price Tracker')

# Button to scrape the current prices and ratio
if st.button('Fetch Prices Now'):
    gold_price = scrape_price('https://www.thesilvermountain.nl/en/gold-price')
    silver_price = scrape_price('https://www.thesilvermountain.nl/en/silver-price')
    ratio = scrape_ratio('https://www.thesilvermountain.nl/en/gold-price')
    current_time = datetime.now()
    
    df = load_data()
    new_data = pd.DataFrame({
        'Timestamp': [current_time],
        'Gold Price': [gold_price],
        'Silver Price': [silver_price],
        'Gold-Silver Ratio': [ratio]
    })
    df = pd.concat([df, new_data], ignore_index=True)
    save_data(df)
    
    st.success(f"Current Gold Price: €{gold_price}")
    st.success(f"Current Silver Price: €{silver_price}")
    st.success(f"Current Gold-Silver Ratio: {ratio}")

# Load and preprocess the data
df = load_data()
if not df.empty:
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df = df.sort_values('Timestamp')

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
            'Gold Price': [
                f"€{df_filtered['Gold Price'].min():.2f}",
                f"€{df_filtered['Gold Price'].max():.2f}",
                f"€{df_filtered['Gold Price'].mean():.2f}"
            ],
            'Silver Price': [
                f"€{df_filtered['Silver Price'].min():.2f}",
                f"€{df_filtered['Silver Price'].max():.2f}",
                f"€{df_filtered['Silver Price'].mean():.2f}"
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
        fig_gold = px.line(df_filtered, x='Timestamp', y='Gold Price', title='Gold Price Over Time')
        st.plotly_chart(fig_gold)

        fig_silver = px.line(df_filtered, x='Timestamp', y='Silver Price', title='Silver Price Over Time')
        st.plotly_chart(fig_silver)

        fig_ratio = px.line(df_filtered, x='Timestamp', y='Gold-Silver Ratio', title='Gold-Silver Ratio Over Time')
        st.plotly_chart(fig_ratio)

        # Display raw data
        st.subheader('Raw Data')
        st.dataframe(df_filtered)

else:
    st.info("No data available. Click 'Fetch Prices Now' to start collecting data.")

# Add some instructions
st.sidebar.header("Instructions")
st.sidebar.info(
    "This app displays the gold and silver prices, and the gold-silver ratio from thesilvermountain.nl. "
    "The data is updated daily at 7:00 AM UTC via GitHub Actions. "
    "Click the 'Fetch Prices Now' button to manually update the data. "
    "Use the date range selector to view statistics and charts for specific time periods. "
    "The app displays price statistics, charts, and raw data for the selected date range."
)
