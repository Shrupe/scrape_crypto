import time
from datetime import datetime
from scraper.main_scraper import fetch_crypto_prices
from database.db_manager import insert_prices, insert_latest_prices
from .plot_history import plot_history

def auto_main(time=15, period=1):
    print(f"Started scraping loop at {datetime.now()}")
    for i in range(0, time, period):
        print(f"Iteration {i+1}/15")
        data = fetch_crypto_prices()
        if data:
            insert_prices(data)
            insert_latest_prices(data)
            print("Data inserted.")
        else:
            print("No data scraped.")
        time.sleep(60)  # wait 60 seconds

    print(f"Finished scraping at {datetime.now()}")
    plot_history()

if __name__ == "__main__":
    auto_main()
    
