import time
from simple_salesforce import Salesforce
import psycopg2
from psycopg2 import Error
import requests

sf_username = 'harshacrypto508@gmail.com'
sf_password = 'Harsha@508'
sf_security_token = '2A01FOGsratz82FEgModsSzh'
sf = Salesforce(username=sf_username, password=sf_password, security_token=sf_security_token)

def get_database_connection():
    connection = psycopg2.connect(
        user="postgres",
        password="Harsha508",
        host="database-1.cigflazwbdyg.ap-south-1.rds.amazonaws.com",
        port="5432",
        database="crypto",
    )
    cursor = connection.cursor()
    return connection, cursor

def get_buy_coins():
    print("Fetching records from database...")  # Add this print statement
    try:
        con, cur = get_database_connection()
        sql = "SELECT symbol, intialPrice, highPrice, lastPrice, margin, purchasePrice, status FROM trading WHERE status = '1'"
        cur.execute(sql)
        rows = cur.fetchall()
        data = [
            {
                "Name": row[0],
                "Initial_price__c": row[1],
                "Highest_Price__c": row[2],
                "Lastest_Price__c": row[3],
                "Margin__c": row[4],
                "Purchase_Price__c": row[5],
                # Add other fields if needed
            }
            for row in rows
        ]
        print(f"Fetched {len(data)} records from database")  # Add this print statement
        return data
    except Exception as e:
        print(e)
    finally:
        con.close()

def get_data_to_insert():
    return get_buy_coins()

def insert_data_into_salesforce(data):
    for record in data:
        try:
            sf.Trading__c.create(record)
            print(f"Record inserted: {record}")
        except Exception as e:
            print(f"Error inserting record: {record}. Exception: {e}")
def run_every_10_minutes():
    print("Starting the loop...")  # Add this print statement
    while True:
        try:
            data = get_data_to_insert()
            if data:  # Check if there's data to insert
                insert_data_into_salesforce(data)
            else:
                print("No data to insert. Waiting for the next iteration...")
        except Exception as e:
            print(f"An error occurred: {e}")

        time.sleep(600)  # 10 minutes in seconds
if __name__ == "__main__":
    print("Starting the script...")  # Add this print statement
    run_every_10_minutes()

