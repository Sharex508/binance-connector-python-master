from tokenize import Double
import requests
import websockets
from binance.spot import Spot as Client
from binance.lib.utils import config_logging 
from datetime import datetime as dt
import time    
import json
import psycopg2
from psycopg2.extras import execute_values
import datetime
import time
import schedule
from notifications import notisend
from concurrent.futures import ThreadPoolExecutor
client = Client()
import re
import pandas as pd
import ccxt




def get_db_connection():
    connection = psycopg2.connect(user="postgres",
                                  password="Harsha508",
                                  host="database-1.cigflazwbdyg.ap-south-1.rds.amazonaws.com",
                                  port="5432",
                                  database="crypto")

    cursor = connection.cursor()
    return connection, cursor

def get_data_from_wazirx(filter='USDT'):
     data = requests.get('https://api.binance.com/api/v3/ticker/price').json()

    # Filter data to include only symbols that contain the currency in the filter.
     resp = [d for d in data if filter in d['symbol'] and 'price' in d]
    
    # Update each dictionary in resp with additional keys.
     for obj in resp:
        lprice = float(obj['price'])
        obj.update({
            "lastPrice" : lprice
            
        })
       # print('completed')
    
     return resp


def get_results():
    connection = None
    try:
        connection = psycopg2.connect(user="postgres",
                                  password="Harsha508",
                                  host="database-1.cigflazwbdyg.ap-south-1.rds.amazonaws.com",
                                  port="5432",
                                  database="crypto")
        connection.autocommit = True

        cursor = connection.cursor()
        sql = "SELECT * FROM trading where status='0'"
        try:

            cursor.execute(sql)
            # Fetch all the rows in a list of lists.
            results = cursor.fetchall()
            keys = ('symbol', 'intialPrice', 'highPrice',
                   'lastPrice', 'margin')
            data = []
            for obj in results:
               data.append(dict(zip(keys, obj)))
             
            return data
            print(data)
        except Exception as e:
            print(e)
    except Exception as e:
            print(e)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

    
def get_diff_of_db_api_values():
    start = time.time()
    db_resp = get_results()
    api_resp = get_data_from_wazirx()
    dicts_data = [obj['symbol'] for obj in db_resp]

    n = 1000
    chunks = [dicts_data[i:i+n] for i in range(0, len(dicts_data), n)]

    with ThreadPoolExecutor(max_workers=6) as executor:
        for chunk in chunks:
            executor.submit(task, db_resp, api_resp, chunk)
            #print(db_resp)

    done = time.time()
    elapsed = done - start
    #print(elapsed)



def task(db_resp, api_resp, data):
    for ele in data:
        db_match_data = next((item for item in db_resp if item["symbol"] == ele), None)
        if not db_match_data:
            continue
        api_match_data = next((item for item in api_resp if item["symbol"] == ele), None)
        if not api_match_data:
            continue
        if api_match_data['symbol'] == db_match_data['symbol']:
            api_last_price = float(api_match_data['lastPrice'])
            db_margin = float(db_match_data['margin'])
            initial_price = float(db_match_data['intialPrice'])

            if api_last_price >= db_margin:
                quantity = 100 / api_last_price
                dbdata = {"symbol": ele, "side": "buy", "type": "limit", "price": api_last_price, "quantity": quantity, "recvWindow": 10000, "timestamp": int(time.time() * 1000)}
                notisend({"symbol": ele, "side": "buy", "type": "limit", "initial_price": initial_price, "purchasing_price": api_last_price, "db_margin": db_margin, "quantity": quantity})
                
                # Update coin record here
                update_coin_record(dbdata)



# Replace these with your Binance API key and secret key
api_key = 'NGhlcbaJhbGBXzim10ij6B6MSpXq19eq5E62MOyHhWPm5sbaBxHAPSfwkOZ1o6CK'
api_secret = 'H3RK3yPS90Foi8uRiFMBkdIpIx1TvHDIqPpDo58ZfLPlAtHclzhOAZME4YZ5Uprj'
client = Client(api_key, api_secret)
# Initialize Binance client with ccxt
binance = ccxt.binance({
    'apiKey': api_key,
    'secret': api_secret
})

# Replace SYMBOL, QUANTITY, and PRICE with your desired values
symbol = 'BNB/USDT'
quantity = 0.1  # The amount of BNB you want to buy
price = 400  # The price at which you want to buy BNB

def create_limit_buy_order(symbol, quantity, price):
    try:
        # Create a limit buy order
        order = binance.create_limit_buy_order(symbol, quantity, price)
        print(f"Limit buy order created: {order}")
    except ccxt.BaseError as e:
        print(f"Error: {e}")
        # this is for limit less order : order = binance.create_market_buy_order(symbol, quantity)




def coin_buy(data):
    try:
        client.send('create_order', data)
        update_coin_record(data)
    except Exception as e:
        print(e)
        notisend(e)

def update_coin_record(dbdata):
    try:
        print("came to database update")
        con = get_db_connection()
        sql= "UPDATE trading_test  SET status = 1 ,purchasePrice= {1} WHERE symbol= {0}".format(repr(dbdata['symbol']), repr(dbdata['price']));
        print(sql)
        con[1].execute(sql)
        con[0].commit()
        print("i was saved")
    except Exception as e:
        print("i was fucked up")
        notisend(e)
        print(e)
    finally:
        con[0].close()

def show():

    while 1:
        get_diff_of_db_api_values()
        time.sleep(10)
show()

