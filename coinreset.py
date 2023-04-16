from cgitb import text
import string
import time
import psycopg2
from psycopg2 import Error
import requests
import websockets
import json
import logging
from binance.spot import Spot as Client
from binance.lib.utils import config_logging 

def table_Delete_crypto():
        try:
            with psycopg2.connect(user="postgres",
                                  password="Harsha508",
                                  host="database-1.cigflazwbdyg.ap-south-1.rds.amazonaws.com",
                                  port="5432",
                                  database="crypto") as conn:
                with conn.cursor() as cursor:
                    cursor.execute("DROP TABLE IF EXISTS trading_test")
                    cursor.execute("DROP TABLE IF EXISTS coin_buy")
                    print("Tables deleted successfully...")
        except psycopg2.Error as e:
            print("Error deleting tables: ", e)


def table_Create_crypto():
    try:
        with psycopg2.connect(user="postgres",
                                  password="Harsha508",
                                  host="database-1.cigflazwbdyg.ap-south-1.rds.amazonaws.com",
                                  port="5432",
                                  database="crypto") as connection:
            with connection.cursor() as cursor:
                # SQL query to create a new table

                create_table_query = '''CREATE TABLE IF NOT EXISTS trading
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
                        ); '''
                cursor.execute(create_table_query)
                print("Table created successfully in PostgreSQL - trading_test")
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL: ", error)

def getall_data(filter='USDT'):
    data = requests.get('https://api.binance.com/api/v3/ticker/price').json()

    # Filter data to include only symbols that contain the currency in the filter.
    resp = [d for d in data if filter in d['symbol'] and 'price' in d]
    
    # Update each dictionary in resp with additional keys.
    for obj in resp:
        lprice = float(obj['price'])
        marg = lprice * 1.03
        obj.update({
            "initialPrice": lprice,
            "highPrice": lprice,
            "margin": marg,
            "purchasePrice": ""
        })

    
    return insert_data_db(resp)

def insert_data_db(resp):
    try:
        connection = psycopg2.connect(user="postgres",
                                  password="Harsha508",
                                  host="database-1.cigflazwbdyg.ap-south-1.rds.amazonaws.com",
                                  port="5432",
                                  database="crypto")
        connection.autocommit = True

        cursor = connection.cursor()
        columns = resp[0].keys()
        query = "INSERT INTO trading_test ({}) VALUES %s".format(
            ','.join(columns))

        # convert projects values to sequence of seqeences
        values = [[value.strip() if type(value) == "str" else str(value)
                               for value in obj.values()] for obj in resp]
        # import pdb;pdb.set_trace()
        tuples = [tuple(x) for x in values]
        cursor.executemany(
    "INSERT INTO trading VALUES(%s,%s,%s,%s,%s,%s)", tuples)
        print("Data Inserted successfully in trading table.......... ")

    except Exception as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


def show():

    while 1:
        table_Delete_crypto()
        table_Create_crypto ()
        getall_data()
        time.sleep(86400)
show()


