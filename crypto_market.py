from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('X_CMC_PRO_API_KEY')

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
    'start': '1',
    'limit': '100',
    'convert': 'USD'
}
headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': api_key,
}

session = Session()
session.headers.update(headers)

try:
    response = session.get(url, params=parameters)
    data = json.loads(response.text)
    sorted_data = sorted(data['data'], key=lambda x: x.get('symbol', '').lower())
    if 'data' in data:
        print("\nName              | Symbol | Price")
        print("-" * 40)
        for crypto in sorted_data:
            symbol = crypto.get('symbol', 'N/A')
            name = crypto.get('name', 'N/A')
            price = crypto.get('quote', {}).get('USD', {}).get('price', 'N/A')
            if price > 0.00:
                print(f"{name[:17]:<17} | {symbol:<6} | ${price:>10.2f}")
except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(f"Error occurred: {e}")