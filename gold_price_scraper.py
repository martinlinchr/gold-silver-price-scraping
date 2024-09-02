import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import plotly.express as px

def scrape_gold_price():
    url = 'https://www.thesilvermountain.nl/en/gold-silver-ratio'
    
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Replace '.gold-price-element' with the correct selector
    gold_price_element = soup.select_one('.gold-price-element')
    
    if gold_price_element:
        gold_price = gold_price_element.text.strip()
    else:
        gold_price = "Price not found"
    
    return gold_price

def load_data():
    try:
        df = pd.read_csv('gold_price_data.csv', names=['Timestamp', 'Price'])
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        return df
    except FileNotFoundError:
        return pd.DataFrame(columns=['Timestamp', 'Price'])

def save_data(df):
    df.to_csv('gold_price_data.csv', index=False, header=False)

st.title('Gold Price Tracker')

# Button to scrape the current price
if st.button('Scrape Current Gold Price'):
    current_price = scrape_gold_price()
    current_time = datetime.now()
    
    df = load_data()
    new_data = pd.DataFrame({'Timestamp': [current_time], 'Price': [current_price]})
    df = pd.concat([df, new_data], ignore_index=True)
    save_data(df)
    
    st.success(f"Current Gold Price: {current_price}")

# Display the data
df = load_data()
if not df.empty:
    st.subheader('Gold Price History')
    st.dataframe(df)
    
    # Create a line chart
    fig = px.line(df, x='Timestamp', y='Price', title='Gold Price Over Time')
    st.plotly_chart(fig)
else:
    st.info("No data available. Click 'Scrape Current Gold Price' to start collecting data.")

# Add some instructions
st.sidebar.header("Instructions")
st.sidebar.info(
    "This app scrapes the current gold price from thesilvermountain.nl. "
    "Click the 'Scrape Current Gold Price' button to update the data. "
    "The app will display the price history and a chart of prices over time."
)
