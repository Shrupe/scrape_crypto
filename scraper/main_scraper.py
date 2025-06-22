from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from datetime import datetime
import time
import shutil
import os
from database.db_manager import insert_prices, insert_latest_prices
import requests

URL_API = "https://api.coingecko.com/api/v3/coins/markets"
URL = 'https://www.coingecko.com/en'
PARAMS = {
    "vs_currency": "usd",
    "order": "market_cap_desc",
    "per_page": 10,
    "page": 1,
    "sparkline": "false"
}

def fetch_crypto_prices():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--user-agent=Mozilla/5.0')

    service = Service(shutil.which("chromedriver"))
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(URL)
    time.sleep(5)  # let JS load

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    table_rows = soup.select('table tbody tr')
    data = []

    for row in table_rows[:10]:  # Top 10 coins
        cols = row.find_all('td')
        try:
            # Extract coin name from column 2
            name = cols[2].text.strip().split('\n')[0]

            # Extract price from column 4 (NOT 3 — 3 is "Buy" button)
            price_text = cols[4].text.strip().replace('$', '').replace(',', '')
            price = float(price_text)

            timestamp = datetime.utcnow()
            data.append((name, price, timestamp))
        except Exception as e:
            print(f"Error parsing row: {e}")
            print([c.text.strip() for c in cols])
            print(f"Raw price text: {cols[4].text.strip()}")
            continue

    return data


def fetch_crypto_prices_api(url=URL, params=PARAMS):
    response = requests.get(url, params)
    data = []

    if response.status_code != 200:
        print("API error:", response.status_code)
        return []

    coins = response.json()
    for coin in coins:
        name = coin["name"]
        price = coin["current_price"]
        timestamp = datetime.now()
        data.append((name, price, timestamp))

    return data

if __name__ == "__main__":  
    #prices = fetch_crypto_prices_api(URL, PARAMS)
    prices = fetch_crypto_prices()
    if prices:
        insert_prices(prices)
        insert_latest_prices(prices)
        print("Inserted prices into database.")
    else:
        print("No data scraped.")
