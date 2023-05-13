
import requests
from binance.spot import Spot as Client
import ccxt

# Set up Binance client
api_key = 'NGhlcbaJhbGBXzim10ij6B6MSpXq19eq5E62MOyHhWPm5sbaBxHAPSfwkOZ1o6CK'
api_secret = 'H3RK3yPS90Foi8uRiFMBkdIpIx1TvHDIqPpDo58ZfLPlAtHclzhOAZME4YZ5Uprj'
client = Client(api_key, api_secret)

def get_wallet_balance():
    # Initialize Binance client with ccxt
    binance = ccxt.binance({
        'apiKey': api_key,
        'secret': api_secret
    })

    try:
        # Get account balances
        balance = binance.fetch_balance()

        # Print wallet balances
        for info in balance['info']['balances']:
            asset = info['asset']
            free = float(info['free'])
            locked = float(info['locked'])
            total = free + locked

            if total > 0:
                print(f"{asset}: {total}")
    except ccxt.BaseError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_wallet_balance()

