import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_price(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    price_element = soup.select_one('small:-soup-contains("PRICE")')
    
    if price_element:
        price = price_element.text.strip()
        price = ''.join(filter(lambda x: x.isdigit() or x == '.', price))
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
    # This block will only run if the script is executed directly (not imported)
    from datetime import datetime
    
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
