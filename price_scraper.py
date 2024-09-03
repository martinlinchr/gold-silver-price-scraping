import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def scrape_price(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Look for the price in the <small> tag
    price_element = soup.select_one('small')
    
    if price_element:
        # Extract the price text
        price_text = price_element.text.strip()
        # Remove the euro symbol and any whitespace
        price = price_text.replace('€', '').strip()
        # Convert to float for consistency
        try:
            price = float(price.replace('.', '').replace(',', '.'))
        except ValueError:
            price = "Price conversion error"
    else:
        price = "Price not found"
    
    return price

def load_data():
    try:
        df = pd.read_csv('metal_price_data.csv')
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        return df
    except FileNotFoundError:
        return pd.DataFrame(columns=['Timestamp', 'Gold Price', 'Silver Price'])

def save_data(df):
    df.to_csv('metal_price_data.csv', index=False)

if __name__ == "__main__":
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

    print(f"Scraping completed. Gold price: €{gold_price}, Silver price: €{silver_price}")
    print("Data appended to metal_price_data.csv")
