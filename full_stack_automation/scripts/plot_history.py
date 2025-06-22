import psycopg2
import matplotlib.pyplot as plt
from datetime import datetime

def get_top_3_latest():
    conn = psycopg2.connect(dbname="crypto_db", user="crypto_user", password="1234", host="localhost")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT name FROM latest_prices
        ORDER BY price DESC
        LIMIT 3
    """)
    top_names = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return top_names

def get_price_history(name):
    conn = psycopg2.connect(dbname="crypto_db", user="crypto_user", password="1234", host="localhost")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT timestamp, price FROM crypto_prices
        WHERE name = %s
        ORDER BY timestamp
    """, (name,))
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def plot_history():
    top_coins = get_top_3_latest()
    plt.figure(figsize=(10, 6))

    for coin in top_coins:
        history = get_price_history(coin)
        times = [row[0] for row in history]
        prices = [row[1] for row in history]
        plt.plot(times, prices, label=coin)

    plt.title("Price History of Top 3 Coins")
    plt.xlabel("Time")
    plt.ylabel("Price (USD)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.xticks(rotation=45)
    plt.savefig("price_history_top3.png")
    plt.show()

if __name__ == "__main__":
    plot_history()
