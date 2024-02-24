import requests
import json


def notisend(msg):
    token = '5514541778:AAGLeivNhJUZvXG43IOo0eyq2SYKs66m6vw'
    userID = 1893850031
    message = json.dumps(msg)
    # Create url
    url = f'https://api.telegram.org/bot{token}/sendMessage'

    # Create json link with message
  #  data = {'chat_id': userID, 'text': message}
    data = {'chat_id': userID, 'text': 'fuuckoff harsha'}
    # POST the message
    requests.post(url, data)
