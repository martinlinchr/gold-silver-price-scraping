import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from price_scraper import scrape_price, scrape_ratio, load_data, save_data

st.title('Gold and Silver Price Tracker')

# Button to scrape the current prices and ratio
if st.button('Scrape Current Data'):
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

# Display the data
df = load_data()
if not df.empty:
    st.subheader('Price and Ratio History')
    st.dataframe(df)
    
    # Create line charts
    fig_gold = px.line(df, x='Timestamp', y='Gold Price', title='Gold Price Over Time')
    st.plotly_chart(fig_gold)
    
    fig_silver = px.line(df, x='Timestamp', y='Silver Price', title='Silver Price Over Time')
    st.plotly_chart(fig_silver)
    
    fig_ratio = px.line(df, x='Timestamp', y='Gold-Silver Ratio', title='Gold-Silver Ratio Over Time')
    st.plotly_chart(fig_ratio)
else:
    st.info("No data available. Click 'Scrape Current Data' to start collecting data.")

# Add some instructions
st.sidebar.header("Instructions")
st.sidebar.info(
    "This app displays the current gold and silver prices, and the gold-silver ratio from thesilvermountain.nl. "
    "The data is updated daily at 7:00 AM UTC via GitHub Actions. "
    "Click the 'Scrape Current Data' button to manually update the data. "
    "The app displays the price and ratio history and charts over time."
)
