import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import mplcursors
from datetime import datetime, timedelta
import argparse
import numpy as np

# Function to convert numeric values to strings with k for thousands, M for millions, etc.
def fmt(x, pos):
    if x == 0:
        return '0'
    elif x >= 1e9:
        return f'{x*1e-9:.0f}B'
    elif x >= 1e6:
        return f'{x*1e-6:.0f}M'
    elif x >= 1e3:
        return f'{x*1e-3:.0f}k'
    else:
        return f'{x:.0f}'



# Function definition to fetch historical data
def fetch_historical_data(crypto_id, vs_currency, from_timestamp, to_timestamp):
    url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}/market_chart/range"
    params = {
        'vs_currency': vs_currency,
        'from': from_timestamp,
        'to': to_timestamp
    }
    response = requests.get(url, params=params)
    data = response.json()
    prices = data['prices']
    df = pd.DataFrame(prices, columns=['timestamp', 'price'])
    df['date'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('date', inplace=True)
    return df



# Function definition to calculate the MA and the multiplier
def calculate_2y_ma_multiplier(df):
    df['MA_2y'] = df['price'].rolling(window=730, min_periods=1).mean()
    df['MA_2y_multiplier'] = df['MA_2y'] * 5
    return df



# Adjust the y-axis ticks to powers of 10, formatted as k, M, etc., based on price range
def adjust_yticks(ax, df):
    price_min, price_max = df['price'].min(), df['price'].max()
    y_min = 10**np.floor(np.log10(price_min))
    y_max = 10**np.ceil(np.log10(price_max))
    yticks = np.logspace(np.log10(y_min), np.log10(y_max), num=int(np.log10(y_max) - np.log10(y_min)) + 1)
    ax.set_yticks(yticks)
    ax.get_yaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(fmt))



# Setting up argparse for command-line arguments
parser = argparse.ArgumentParser(description='2-Year MA Multiplier for Cryptocurrency.')
parser.add_argument('crypto_id', type=str, help='The id of the cryptocurrency (e.g., bitcoin)')
parser.add_argument('--currency', type=str, help='The currency to compare against (e.g., usd)', default='usd')
parser.add_argument('--from_date', type=str, help='Start date in YYYY-MM-DD format')
parser.add_argument('--to_date', type=str, help='End date in YYYY-MM-DD format')
parser.add_argument('--include_halvings', action='store_true', help='Include BTC halving dates in the graph')


# Parsing arguments
args = parser.parse_args()

# Current date
current_date = datetime.now()

if args.from_date and args.to_date:
    from_timestamp = int(datetime.strptime(args.from_date, '%Y-%m-%d').timestamp())
    to_timestamp = int(datetime.strptime(args.to_date, '%Y-%m-%d').timestamp())
else:
    # Set from_date to 2 years ago from the current date
    from_date = current_date - timedelta(days=730)
    to_date = current_date
    from_timestamp = int(from_date.timestamp())
    to_timestamp = int(to_date.timestamp())

# Fetching and processing data
df = fetch_historical_data(args.crypto_id, args.currency, from_timestamp, to_timestamp)
df = calculate_2y_ma_multiplier(df)

# Plotting the graph with logarithmic scale on the Y-axis
plt.figure(figsize=(14, 7))
price_line, = plt.plot(df.index, df['price'], label=f'{args.crypto_id.capitalize()} Price', color='black')
ma_line, = plt.plot(df.index, df['MA_2y'], label='2-Year MA', color='green')
ma_multiplier_line, = plt.plot(df.index, df['MA_2y_multiplier'], label='2-Year MA x5', color='red', linestyle='--')

# Use fill_between to highlight the area where the price is below the 2-Year MA to indicate to buy
plt.fill_between(df.index, df['price'], df['MA_2y'], where=(df['price'] < df['MA_2y']), color='green', alpha=0.3, label='Buy indicator')

# Use fill_between to highlight the area where the price is over the 2-Year MA * 5 to indicate to sell
plt.fill_between(df.index, df['price'], df['MA_2y_multiplier'], where=(df['price'] > df['MA_2y_multiplier']), color='red', alpha=0.3, label='Sell indicator')

if args.include_halvings:
    halving_dates = ['2012-11-28', '2016-07-09', '2020-05-11']
    halving_labels = ['1st Halving', '2nd Halving', '3rd Halving']

    # Add vertical lines for halving dates
    for date, label in zip(halving_dates, halving_labels):
        plt.axvline(x=pd.to_datetime(date), color='k', linestyle='--', linewidth=1)
        plt.text(pd.to_datetime(date), plt.ylim()[1], label, horizontalalignment='right', verticalalignment='top')

plt.yscale('log')  # Sets the Y-axis to a logarithmic scale

adjust_yticks(plt.gca(), df)

plt.title(f'2-Year MA Multiplier for {args.crypto_id.capitalize()} in {args.currency.upper()}')
plt.xlabel('Date')
plt.ylabel(f'Price in {args.currency.upper()} (Logarithmic Scale)')
plt.legend()
plt.grid(True, which="both", ls="--")  # Adds a grid and ensures it is shown for both major and minor scales

# Adding interactivity with mplcursors
cursor = mplcursors.cursor([price_line, ma_line, ma_multiplier_line], hover=True)

@cursor.connect("add")
def on_add(sel):
    x, y = sel.target
    date_str = matplotlib.dates.num2date(x).strftime("%Y-%m-%d")
    sel.annotation.set(text=f'Date: {date_str}\nValue: {y:.2f}')
    sel.annotation.get_bbox_patch().set(fc="white", alpha=0.6)


plt.show()
