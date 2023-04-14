import sys
import time
from datetime import datetime, timedelta
from multiprocessing import Process

import psycopg2
import requests
import websockets
from binance.spot import Spot as Client
from psycopg2.extras import execute_values

api_key = "YOUR_API_KEY"
secret_key = "YOUR_SECRET_KEY"


def get_db_connection():
    connection = psycopg2.connect(user="postgres",
                                  password="harsha508",
                                  host="database-1.cigflazwbdyg.ap-south-1.rds.amazonaws.com",
                                  port="5432",
                                  database="crypto"
    )

    cursor = connection.cursor()
    return connection, cursor


def get_buy_coins():
    try:
        con = get_db_connection()
        sql = "SELECT symbol, retrycount FROM trading_test WHERE status = '1'"
        con[1].execute(sql)
        rows = con[1].fetchall()
    except Exception as e:
        print(e)
    finally:
        con[0].close()

    coin_names = [row[0] for row in rows]
    retry_counts = [row[1] for row in rows]

    update_order_status(coin_names)
    reset_order_status(coin_names, retry_counts)


def update_order_status(coin_names):
    client = Client(api_key=api_key, secret_key=secret_key)

    for name in coin_names:
        resp = client.send(
            "open_orders",
            {"symbol": name, "recvWindow": 10000, "timestamp": int(time.time() * 1000)},
        )

        if resp[1][0]["status"] == "success":
            try:
                con = get_db_connection()
                now = datetime.now()
                created_at = now.strftime("%Y-%m-%d %H:%M:%S")
                margin_time = (now + timedelta(hours=5)).strftime("%Y-%m-%d %H:%M:%S")
                sql = (
                    "UPDATE trading_test SET status = '2', created_at = %s, "
                    "margin_time = %s, ap_margin = purchasePrice * 1.05 WHERE symbol = %s"
                )
                con[1].execute(sql, (created_at, margin_time, name))
                con[0].commit()
            except Exception as e:
                print(e)
            finally:
                con[0].close()


def reset_order_status(coin_names, retry_counts):
    client = Client(api_key=api_key, secret_key=secret_key)

    for name, rt in zip(coin_names, retry_counts):
        resp = client.send(
            "open_orders",
            {"symbol": name, "recvWindow": 10000, "timestamp": int(time.time() * 1000)},
        )

        if resp[1][0]["status"] != "success":
            try:
                con = get_db_connection()
                sql = (
                    "UPDATE trading_test SET status = '0', retrycount = %s "
                    "WHERE symbol = %s"
                )
                con[1].execute(sql, (rt, name))
                con[0].commit()
            except Exception as e:
                print(e)
            finally:
                con[0].close()


def run1():
    while True:
        get_buy_coins()
        time.sleep(10)


if __name__ == "__main__":
    run1()
