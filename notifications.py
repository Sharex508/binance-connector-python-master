import requests
import json

def notisend(msg):
    token = '6883463112:AAGTCi7kkguV2-3e_4HMR2vD75WjLbqce7U'
    userID = 1893850031  # Replace with your user ID

    # Create URL for sending messages
    url = f'https://api.telegram.org/bot{token}/sendMessage'

    # Create data payload as a dictionary
    data = {'chat_id': userID, 'text': msg}

    # Send POST request to the Telegram API with JSON data
    response = requests.post(url, json=data)

    # Check if the request was successful
    if response.status_code == 200:
        print('Message sent successfully!')
    else:
        print(f'Failed to send message. Status code: {response.status_code}')

# Example usage:
#notisend('Hello, world! This is a test message from my Telegram bot.')
