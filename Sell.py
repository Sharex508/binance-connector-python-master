import time
import psycopg2
from ccxt import binance
from notifications import notisend


api_key = 'NGhlcbaJhbGBXzim10ij6B6MSpXq19eq5E62MOyHhWPm5sbaBxHAPSfwkOZ1o6CK'
api_secret = 'H3RK3yPS90Foi8uRiFMBkdIpIx1TvHDIqPpDo58ZfLPlAtHclzhOAZME4YZ5Uprj'
client = binance({
    'apiKey': api_key,
    'secret': api_secret
})

def get_db_connection():
    connection = psycopg2.connect(
        user="postgres",
        password="Harsha508",
        host="database-1.cigflazwbdyg.ap-south-1.rds.amazonaws.com",
        port="5432",
        database="crypto",
    )
    cursor = connection.cursor()
    return connection, cursor

def get_open_orders():
    connection, cursor = get_db_connection()
    try:
        sql = "SELECT symbol, purchasePrice, highPrice, quantity FROM trading WHERE status = '1'"
        cursor.execute(sql)
        rows = cursor.fetchall()
        return rows
    except Exception as e:
        print(e)
    finally:
        connection.close()

def get_binance_prices(symbols):
    tickers = client.fetch_tickers(symbols)
    return {symbol: ticker['last'] for symbol, ticker in tickers.items()}

def update_stop_loss(client, symbol, quantity, stop_loss_price, limit_price):
    try:
        order = client.create_order(
            symbol=symbol,
            side='SELL',
            type='STOP_LOSS_LIMIT',
            timeInForce='GTC',
            quantity=quantity,
            stopPrice=stop_loss_price,
            price=limit_price
        )
        print(f"Stop loss limit order updated: {order}")
        notisend("order updated"+{order})
    except Exception as e:
        print(f"Error updating stop loss limit order: {e}")

def run_stop_loss_update_loop():
    while True:
        try:
            open_orders = get_open_orders()
            symbols = [row[0] for row in open_orders]
            binance_prices = get_binance_prices(symbols)
            
            for order in open_orders:
                symbol, purchase_price, high_price, quantity = order
                last_price = binance_prices[symbol]
                stop_loss_price = max(purchase_price * 0.97, high_price * 0.97)
                limit_price = stop_loss_price * 0.99
                update_stop_loss(client, symbol, quantity, stop_loss_price, limit_price)
            time.sleep(60)
        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(10)

if __name__ == "__main__":
    run_stop_loss_update_loop()
