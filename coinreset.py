import time
import psycopg2
from psycopg2 import Error
import requests
import logging

logging.basicConfig(level=logging.INFO)
import os
from dotenv import load_dotenv

load_dotenv()

def get_database_connection():
    return psycopg2.connect(
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        database=os.getenv("POSTGRES_DB"),
    )


def table_Delete_crypto():
    try:
        with get_database_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM trading_test")
                logging.info("Rows deleted successfully...")
    except psycopg2.Error as e:
        logging.error(f"Error deleting rows: {e}")


def table_Create_crypto():
    try:
        with get_database_connection() as connection:
            with connection.cursor() as cursor:
                create_table_query = '''
                    CREATE TABLE IF NOT EXISTS trading
                    (
                    symbol            TEXT    NOT NULL,
                    intialPrice       TEXT,
                    highPrice         TEXT,
                    lastPrice         TEXT,
                    margin            TEXT,
                    purchasePrice     TEXT,
                    ap_margin         TEXT,
                    sell_Margin       TEXT,
                    created_at        TEXT,
                    marggin_time      Text,
                    retrycount        Integer,
                    sellretrycount    Integer,
                    status            TEXT  DEFAULT '0'
                    );
                '''
                cursor.execute(create_table_query)
                logging.info("Table created successfully in PostgreSQL - trading_test")
    except (Exception, Error) as error:
        logging.error(f"Error while connecting to PostgreSQL: {error}")


def getall_data(filter='USDT'):
    data = requests.get('https://api.binance.com/api/v3/ticker/price').json()

    resp = [d for d in data if filter in d['symbol'] and 'price' in d]

    for obj in resp:
        lprice = float(obj['price'])
        marg = lprice * 1.03
        obj.update({
            "initialPrice": lprice,
            "highPrice": lprice,
            "margin": marg,
            "purchasePrice": ""
        })
        logging.info('completed')

    return resp


def insert_data_db(resp):
    try:
        with get_database_connection() as connection:
            connection.autocommit = True

            with connection.cursor() as cursor:
                columns = resp[0].keys()
                query = "INSERT INTO trading_test ({}) VALUES %s".format(
                    ','.join(columns))

                values = [
                    [value.strip() if isinstance(value, str) else str(value) for value in obj.values()]
                    for obj in resp
                ]
                tuples = [tuple(x) for x in values]
                cursor.executemany(
                    "INSERT INTO trading VALUES(%s,%s,%s,%s,%s,%s)", tuples)
                logging.info("Data Inserted successfully in trading table.......... ")

    except Exception as error:
        logging.error(f"Error while connecting to PostgreSQL: {error}")



def main():
    while True:
        table_Delete_crypto()
        table_Create_crypto()
        data = getall_data()
        insert_data_db(data)
        time.sleep(86400)

if __name__ == "__main__":
    main()


