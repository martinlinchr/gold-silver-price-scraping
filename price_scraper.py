import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from io import StringIO

def scrape_price(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    price_element = soup.select_one('small')
    if price_element:
        price_text = price_element.text.strip()
        price = price_text.replace('€', '').strip()
        try:
            price = float(price.replace('.', '').replace(',', '.'))
        except ValueError:
            price = "Price conversion error"
    else:
        price = "Price not found"
    
    return price

def scrape_ratio(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    ratio_label = soup.find('div', string='Gold-silver ratio')
    if ratio_label:
        ratio_element = ratio_label.find_next_sibling('div', class_='text-right')
        if ratio_element:
            ratio = ratio_element.text.strip()
            try:
                ratio = float(ratio)
            except ValueError:
                ratio = "Ratio conversion error"
        else:
            ratio = "Ratio not found"
    else:
        ratio = "Ratio not found"
    
    return ratio

def load_data():
    try:
        df = pd.read_csv('metal_price_data.csv')
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        return df
    except FileNotFoundError:
        return pd.DataFrame(columns=['Timestamp', 'Gold Price', 'Silver Price', 'Gold-Silver Ratio'])

def save_data(df):
    df.to_csv('metal_price_data.csv', index=False)

if __name__ == "__main__":
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

    print(f"Scraping completed. Gold price: €{gold_price}, Silver price: €{silver_price}, Gold-Silver Ratio: {ratio}")
    print("Data appended to metal_price_data.csv")
