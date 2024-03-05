import requests
import argparse

# Setting up argparse to accept command line arguments
parser = argparse.ArgumentParser(description='Fetch crypto data or list all coin IDs.')
parser.add_argument('crypto_ids', nargs='*', help='List of crypto IDs', default=None)
parser.add_argument('--currency', help='Currency code', default='usd')
parser.add_argument('--list', help='List all available coin IDs from CoinGecko', action='store_true')

args = parser.parse_args()

def list_all_coins():
    url = 'https://api.coingecko.com/api/v3/coins/list'
    response = requests.get(url)
    coins = response.json()
    for coin in coins:
        id = coin['id']
        name = coin['name']
        symbol = coin['symbol']
        print(f"{name} - {id} - {symbol}")



def fetch_crypto_data(crypto_ids, currency):
    url = 'https://api.coingecko.com/api/v3/coins/markets'
    params = {
        'vs_currency': currency,
        'ids': ','.join(crypto_ids),
    }
    response = requests.get(url, params=params)
    data = response.json()

    for coin in data:
        name = coin['name']
        current_price = coin['current_price']
        total_volume = coin['total_volume']
        volume_change_24h = coin['price_change_percentage_24h']
        print(f"{name}: Price: {current_price} {currency.upper()}, 24h Volume: {total_volume} {currency.upper()}, Volume Change: {volume_change_24h}%")


if args.list:
    list_all_coins()
elif args.crypto_ids:
    fetch_crypto_data(args.crypto_ids, args.currency)
else:
    parser.print_help()
