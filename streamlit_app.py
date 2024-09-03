import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from price_scraper import scrape_price, load_data, save_data

st.title('Gold and Silver Price Tracker')

# Button to scrape the current prices
if st.button('Scrape Current Prices'):
    gold_price = scrape_price('https://www.thesilvermountain.nl/en/gold-price')
    silver_price = scrape_price('https://www.thesilvermountain.nl/en/silver-price')
    current_time = datetime.now()
    
    df = load_data()
    new_data = pd.DataFrame({
        'Timestamp': [current_time],
        'Gold Price': [gold_price],
        'Silver Price': [silver_price]
    })
    df = pd.concat([df, new_data], ignore_index=True)
    save_data(df)
    
    st.success(f"Current Gold Price: €{gold_price}")
    st.success(f"Current Silver Price: €{silver_price}")

# Display the data
df = load_data()
if not df.empty:
    st.subheader('Price History')
    st.dataframe(df)
    
    # Create line charts
    fig_gold = px.line(df, x='Timestamp', y='Gold Price', title='Gold Price Over Time')
    st.plotly_chart(fig_gold)
    
    fig_silver = px.line(df, x='Timestamp', y='Silver Price', title='Silver Price Over Time')
    st.plotly_chart(fig_silver)
else:
    st.info("No data available. Click 'Scrape Current Prices' to start collecting data.")

# Add some instructions
st.sidebar.header("Instructions")
st.sidebar.info(
    "This app scrapes the current gold and silver prices from thesilvermountain.nl. "
    "Click the 'Scrape Current Prices' button to update the data. "
    "The app will display the price history and charts of prices over time."
)
