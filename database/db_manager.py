import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def insert_prices(data):
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    cur = conn.cursor()

    for name, price, timestamp in data:
        cur.execute(
            "INSERT INTO crypto_prices (name, price, timestamp) VALUES (%s, %s, %s)",
            (name, price, timestamp)
        )

    conn.commit()
    cur.close()
    conn.close()

def insert_latest_prices(data):
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    cursor = conn.cursor()
    for name, price, timestamp in data:
        cursor.execute("""
            INSERT INTO latest_prices (name, price, timestamp)
            VALUES (%s, %s, %s)
            ON CONFLICT (name)
            DO UPDATE SET price = EXCLUDED.price, timestamp = EXCLUDED.timestamp
        """, (name, price, timestamp))
    conn.commit()
    cursor.close()
    conn.close()
