import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

def scrape_gold_price():
    url = 'https://www.thesilvermountain.nl/en/gold-silver-ratio'
    
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Create a BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the element containing the gold price
    # Note: You may need to inspect the website's HTML to find the correct selector
    gold_price_element = soup.select_one('.gold-price-element')  # Replace with the correct selector
    
    if gold_price_element:
        gold_price = gold_price_element.text.strip()
    else:
        gold_price = "Price not found"
    
    return gold_price

def save_to_csv(data, filename):
    with open(filename, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(data)

# Scrape the gold price
gold_price = scrape_gold_price()

# Get current date and time
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Save the data to a CSV file
save_to_csv([current_time, gold_price], 'gold_price_data.csv')

print(f"Scraping completed. Gold price: {gold_price}")
print("Data appended to gold_price_data.csv")
