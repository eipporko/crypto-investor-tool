import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import mplcursors
from datetime import datetime
import argparse

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

# Setting up argparse for command-line arguments
parser = argparse.ArgumentParser(description='2-Year MA Multiplier for Cryptocurrency.')
parser.add_argument('crypto_id', type=str, help='The id of the cryptocurrency (e.g., bitcoin)')
parser.add_argument('vs_currency', type=str, help='The currency to compare against (e.g., usd)')
parser.add_argument('from_date', type=str, help='Start date in YYYY-MM-DD format')
parser.add_argument('to_date', type=str, help='End date in YYYY-MM-DD format')

# Parsing arguments
args = parser.parse_args()

# Converting dates to timestamps
from_timestamp = int(datetime.strptime(args.from_date, '%Y-%m-%d').timestamp())
to_timestamp = int(datetime.strptime(args.to_date, '%Y-%m-%d').timestamp())

# Fetching and processing data
df = fetch_historical_data(args.crypto_id, args.vs_currency, from_timestamp, to_timestamp)
df = calculate_2y_ma_multiplier(df)

# Plotting the graph with logarithmic scale on the Y-axis
plt.figure(figsize=(14, 7))
price_line, = plt.plot(df.index, df['price'], label='BTC Price', color='black')
ma_line, = plt.plot(df.index, df['MA_2y'], label='2-Year MA', color='green')
ma_multiplier_line, = plt.plot(df.index, df['MA_2y_multiplier'], label='2-Year MA x5', color='red', linestyle='--')

# Use fill_between to highlight the area where the price is below the 2-Year MA to indicate to buy
plt.fill_between(df.index, df['price'], df['MA_2y'], where=(df['price'] < df['MA_2y']), color='green', alpha=0.3, label='Buy indicator')

# Use fill_between to highlight the area where the price is over the 2-Year MA * 5 to indicate to sell
plt.fill_between(df.index, df['price'], df['MA_2y_multiplier'], where=(df['price'] > df['MA_2y_multiplier']), color='red', alpha=0.3, label='Sell indicator')


halving_dates = ['2012-11-28', '2016-07-09', '2020-05-11']
halving_labels = ['1st Halving', '2nd Halving', '3rd Halving']

# Add vertical lines for halving dates
for date, label in zip(halving_dates, halving_labels):
    plt.axvline(x=pd.to_datetime(date), color='k', linestyle='--', linewidth=1)
    plt.text(pd.to_datetime(date), plt.ylim()[1], label, horizontalalignment='right', verticalalignment='top')

plt.yscale('log')  # Sets the Y-axis to a logarithmic scale

# Setting the Y-axis ticks to 1k, 10k, 100k, etc.
yticks = [1000, 10000, 100000, 1000000]
ytick_labels = ['1k$', '10k$', '100k$', '1M$']
plt.yticks(yticks, ytick_labels)

plt.title('2-Year MA Multiplier for Bitcoin with Logarithmic Scale')
plt.xlabel('Date')
plt.ylabel('Price in USD (Logarithmic Scale)')
plt.legend()
plt.grid(True, which="both", ls="--")  # Adds a grid and ensures it is shown for both major and minor scales

# Adding interactivity with mplcursors
cursor = mplcursors.cursor([price_line, ma_line, ma_multiplier_line], hover=True)

@cursor.connect("add")
def on_add(sel):
    x, y = sel.target
    # Assuming x is a timestamp in matplotlib's internal format, convert it to a readable date string
    date_str = matplotlib.dates.num2date(x).strftime("%Y-%m-%d")
    sel.annotation.set(text=f'Date: {date_str}\nValue: {y:.2f}')
    sel.annotation.get_bbox_patch().set(fc="white", alpha=0.6)


plt.show()
