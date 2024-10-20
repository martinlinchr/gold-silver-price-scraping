import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import requests
from bs4 import BeautifulSoup

def scrape_price(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    price_element = soup.select_one('small')
    if price_element:
        price_text = price_element.text.strip()
        price = price_text.replace('€', '').strip()
        try:
            return float(price.replace('.', '').replace(',', '.'))
        except ValueError:
            return None
    return None

def scrape_ratio(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    ratio_label = soup.find('div', string='Gold-silver ratio')
    if ratio_label:
        ratio_element = ratio_label.find_next_sibling('div', class_='text-right')
        if ratio_element:
            ratio = ratio_element.text.strip()
            try:
                return float(ratio)
            except ValueError:
                return None
    return None

def fetch_prices():
    gold_price = scrape_price('https://www.thesilvermountain.nl/en/gold-price')
    silver_price = scrape_price('https://www.thesilvermountain.nl/en/silver-price')
    ratio = scrape_ratio('https://www.thesilvermountain.nl/en/gold-price')
    current_time = datetime.now()
    
    return pd.DataFrame({
        'Timestamp': [current_time],
        'Gold Price': [gold_price],
        'Silver Price': [silver_price],
        'Gold-Silver Ratio': [ratio]
    })

st.title('Gold and Silver Price Tracker')

# Button to fetch current prices
if st.button('Fetch Current Prices'):
    with st.spinner('Fetching latest prices...'):
        df = fetch_prices()
    
    if not df.empty and df['Gold Price'].notna().all() and df['Silver Price'].notna().all():
        st.success('Prices fetched successfully!')
        
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
        
        # Create line charts
        st.subheader('Price and Ratio Charts')
        fig_gold = px.line(df, x='Timestamp', y='Gold Price', title='Gold Price (1000g)')
        st.plotly_chart(fig_gold)
        fig_silver = px.line(df, x='Timestamp', y='Silver Price', title='Silver Price (1000g)')
        st.plotly_chart(fig_silver)
        fig_ratio = px.line(df, x='Timestamp', y='Gold-Silver Ratio', title='Gold-Silver Ratio')
        st.plotly_chart(fig_ratio)
        
        # Display raw data
        st.subheader('Raw Data')
        st.dataframe(df)
    else:
        st.error('Failed to fetch prices. Please try again later.')

# Add some instructions
st.sidebar.header("Instructions")
st.sidebar.info(
    "This app displays the current gold and silver prices, and the gold-silver ratio from thesilvermountain.nl. "
    "Click the 'Fetch Current Prices' button to get the latest data. "
    "The app will display the latest prices for different weights, charts, and raw data."
)
