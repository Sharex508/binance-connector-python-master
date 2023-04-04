import psycopg2
from datetime import datetime as dt
from psycopg2 import Error
from binance.spot import Spot as Client
from binance.lib.utils import config_logging
import requests


def get_data_from_wazirx(filter='USDT'):
    data = requests.get('https://api.binance.com/api/v3/ticker/price').json()

    # Filter data to include only symbols that contain the currency in the filter.
    resp = [d for d in data if filter in d['symbol'] and 'price' in d]
    
    # Update each dictionary in resp with additional keys.
    for obj in resp:
        lprice = float(obj['price'])
        obj.update({
            "lastPrice": lprice
        })
    
    return resp


def purchased_coins():
    try:
        connection = psycopg2.connect(user="postgres",
                                       password="Twins@2018",
                                       host="127.0.0.1",
                                       port="5432",
                                       database="wazirx")
        connection.autocommit = True

        cursor = connection.cursor()
        sql = "SELECT * FROM trading_test where status='2'"
        try:
            cursor.execute(sql)
            # Fetch all the rows in a list of lists.
            results = cursor.fetchall()
            keys = ('symbol', 'intialPrice', 'highPrice',
                    'lastPrice', 'bp_margin', 'purchasePrice',
                    'ap_margin', 'sell_Margin', 'created_at',
                    'marggin_time', 'retrycount', 'sellretrycount', 'status')
        
            data = []
            for obj in results:
                data.append(dict(zip(keys, obj)))
            return data

        except Exception as e:
            print(e)
    except Exception as e:
        print(e)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")




def coin_type():
    purchased_data = purchased_coins()
    wazirx_data = get_data_from_wazirx()
    coin_type_dict = {}

    for obj in purchased_data:
        coin_symbol = obj['symbol'].replace('USDT', '')
        for wazirx_obj in wazirx_data:
            if coin_symbol == wazirx_obj['symbol']:
                # Check if the coin is normal or surge
                current_time = dt.now()
                marggin_time = obj['marggin_time']
                last_price = wazirx_obj['lastPrice']
                ap_margin = obj['ap_margin']
                if current_time < marggin_time:
                    if last_price < ap_margin:
                        coin_type = 'normal'
                    else:
                        coin_type = 'surge'
                else:
                    coin_type = 'unknown'
                coin_type_dict[coin_symbol] = {'quoteAsset': wazirx_obj['quoteAsset'], 'type': coin_type}
                break

    return coin_type_dict




