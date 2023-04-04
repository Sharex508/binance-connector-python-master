import requests
import websockets
from binance.spot import Spot as Client
from binance.lib.utils import config_logging 
import json
import psycopg2
from psycopg2.extras import execute_values
import datetime
import time
from multiprocessing import Process
from datetime import datetime, timedelta
import sys

def get_db_connection():
    connection = psycopg2.connect(user="postgres",
                                  password="harsha508",
                                  host="localhost",
                                  port="5432",
                                  database="crypto")

    cursor = connection.cursor()
    return connection, cursor

def get_buy_coins():
    print("enterd 1")
    names = []
    rtcounts = []
    try:
        con = get_db_connection()
        sql = "SELECT symbol, retrycount FROM trading_test WHERE status = '1'"
        con[1].execute(sql)
        rows = con[1].fetchall()
        for name in rows:
            names.append(name[0])
        for rtcount in rows:
            rtcounts.append(rtcount[0])
    except Exception as e:
            print (e)
    finally:
            con[0].close()
    get_open_order_status(names)
    get_open_order_reset(rtcounts)




def get_open_order_status(names):
    print("entered 2")
    api_key = "test_api_key"
    api_key = "1Xdwd3vszGCIqQUrTOX2WPF6txeQg8pPb2Qkl5553XUuqEePJFOS2WDrxdpoFV3W"
    secret_key = "test_secret_key"
    secret_key = "5pG94NHjWycxA5ljZ2oNYcX08utpUT7xJothuNjd"
    client = Client(api_key=api_key, secret_key=secret_key)
    coin_names = names
    print(coin_names)
    if coin_names:
        for name in coin_names:
            if(len(name) > 0):
                resp = client.send('open_orders',
                {"symbol": name, "recvWindow": 10000,
                    "timestamp": int(time.time() * 1000)})
                print(resp)
                if resp[1][0]['status'] == "success":
                    try:
                        con = get_db_connection()
                        now = datetime.now()
                        created_at = now.strftime('%Y-%m-%d %H:%M:%S')
                        margin_time = (now + timedelta(hours=5)).strftime('%Y-%m-%d %H:%M:%S')
                        sql = "UPDATE trading_test SET status = '2', created_at = %s, margin_time = %s, ap_margin = purchasePrice * 1.05 WHERE symbol = %s"
                        con[1].execute(sql, (created_at, margin_time, name))
                        sql4 = ""
                        con[0].commit()
                    except Exception as e:
                        print(e)
                    finally:
                        con[0].close()


def get_open_order_status(names):
    print("enterd 2")
    api_key = "test_api_key"
    api_key = "1Xdwd3vszGCIqQUrTOX2WPF6txeQg8pPb2Qkl5553XUuqEePJFOS2WDrxdpoFV3W"
    secret_key = "test_secret_key"
    secret_key = "5pG94NHjWycxA5ljZ2oNYcX08utpUT7xJothuNjd"
    client = Client(api_key=api_key, secret_key=secret_key)
    coin_names = names
    print(coin_names)
    if coin_names:
        for name in coin_names:
            if(len(name) > 0):
                resp = client.send('open_orders',
                {"symbol": name, "recvWindow": 10000,
                    "timestamp": int(time.time() * 1000)})
                print(resp)
                if resp[1][0]['status'] == "success":
                    try:
                        con=get_db_connection()
                        sql="UPDATE trading_test  SET status = '2' WHERE symbol={0}".format(
                            repr(name))
                        con[1].execute(sql)
                        sql4 = ""
                        con[0].commit()
                    except Exception as e:
                        print (e)
                    finally:
                        con[0].close()

def get_open_order_reset(rtcounts):
    print("enterd 3")
    api_key = "test_api_key"
    api_key = "1Xdwd3vszGCIqQUrTOX2WPF6txeQg8pPb2Qkl5553XUuqEePJFOS2WDrxdpoFV3W"
    secret_key = "test_secret_key"
    secret_key = "5pG94NHjWycxA5ljZ2oNYcX08utpUT7xJothuNjd"
    client = Client(api_key=api_key, secret_key=secret_key)
    coin_names = get_buy_coins()
    if coin_names:
        for name in coin_names:
            if(len(name) > 0):
                rt = rtcounts
                resp = client.send('open_orders',
                {"symbol": "shibinr", "recvWindow": 10000,
                    "timestamp": int(time.time() * 1000)})
                if resp[1][0]['status'] != "success":
                    try:
                        con=get_db_connection()
                        sql="UPDATE trading_test  SET status = '0', retrycount = rt WHERE symbol={0}".format(
                            repr(name))
                        con[1].execute(sql)
                        sql4 = ""
                        con[0].commit()
                    except Exception as e:
                        print (e)
                    finally:
                        con[0].close()
def run1 () :
    while 1:
        get_buy_coins()
        time.sleep(10)

run1()

