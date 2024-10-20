from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
from datetime import datetime

app = Flask(__name__)

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

@app.route('/scrape', methods=['GET'])
def scrape():
    gold_price_1000g = scrape_price('https://www.thesilvermountain.nl/en/gold-price')
    silver_price_1000g = scrape_price('https://www.thesilvermountain.nl/en/silver-price')
    ratio = scrape_ratio('https://www.thesilvermountain.nl/en/gold-price')
    current_time = datetime.now().isoformat()

    if gold_price_1000g is not None and silver_price_1000g is not None:
        data = {
            'timestamp': current_time,
            'gold_price_1000g': gold_price_1000g,
            'gold_price_100g': gold_price_1000g / 10,
            'gold_price_1g': gold_price_1000g / 1000,
            'silver_price_1000g': silver_price_1000g,
            'silver_price_100g': silver_price_1000g / 10,
            'silver_price_1g': silver_price_1000g / 1000,
            'gold_silver_ratio': ratio
        }
        return jsonify(data), 200
    else:
        return jsonify({'error': 'Failed to fetch prices'}), 500

if __name__ == '__main__':
    app.run(debug=True)
